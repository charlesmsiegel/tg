# Multi-Agent Patterns Reference

Advanced patterns for orchestrating multiple agents.

## Agents as Tools (Hierarchical Delegation)

Transform agents into callable tools for an orchestrator:

```python
from strands import Agent, tool
from strands_tools import retrieve, http_request

RESEARCH_PROMPT = """You are a research specialist. Focus on factual, well-sourced information.
Always cite your sources."""

@tool
def research_assistant(query: str) -> str:
    """Process research queries with factual information.
    
    Args:
        query: A research question requiring factual information
    
    Returns:
        Detailed research answer with citations
    """
    research_agent = Agent(
        system_prompt=RESEARCH_PROMPT,
        tools=[retrieve, http_request]
    )
    return str(research_agent(query))

@tool
def code_assistant(task: str) -> str:
    """Handle coding tasks and technical questions.
    
    Args:
        task: Programming task or technical question
    
    Returns:
        Code solution with explanation
    """
    code_agent = Agent(
        system_prompt="You are an expert programmer. Write clean, documented code."
    )
    return str(code_agent(task))

@tool
def writing_assistant(request: str) -> str:
    """Create polished written content.
    
    Args:
        request: Writing task description
    
    Returns:
        Polished written content
    """
    writer_agent = Agent(
        system_prompt="You are a professional writer. Create clear, engaging content."
    )
    return str(writer_agent(request))

# Orchestrator routes to specialists
orchestrator = Agent(
    system_prompt="""You are an intelligent assistant that routes requests to specialists.
    Analyze each request and delegate to the appropriate expert.""",
    tools=[research_assistant, code_assistant, writing_assistant]
)

result = orchestrator("Research quantum computing and write a summary, then create a Python simulation")
```

## Swarm (Emergent Collaboration)

Agents autonomously collaborate with shared context:

```python
from strands import Agent
from strands.multiagent import Swarm
from strands_tools import memory, http_request

# Create specialized agents
researcher = Agent(
    name="researcher",
    system_prompt="""You are a thorough researcher. 
    When you have gathered enough information, hand off to the analyst.""",
    tools=[http_request, memory]
)

analyst = Agent(
    name="analyst", 
    system_prompt="""You analyze information and identify patterns.
    When analysis is complete, hand off to the writer.""",
    tools=[memory]
)

writer = Agent(
    name="writer",
    system_prompt="""You write clear, comprehensive reports.
    Synthesize all gathered information into a final output.""",
    tools=[memory]
)

# Create swarm - first agent receives initial request
swarm = Swarm(
    [researcher, analyst, writer],
    entry_point="researcher"  # Optional, defaults to first agent
)

# Execute with streaming
async for event in swarm.stream_async("Analyze AI industry trends for 2025"):
    if event.type == "handoff":
        print(f"Handoff: {event.from_agent} -> {event.to_agent}")
    elif event.type == "text":
        print(event.data, end="")

# Or synchronous
result = swarm("Analyze AI industry trends for 2025")
```

### Swarm Configuration

```python
swarm = Swarm(
    agents=[agent1, agent2, agent3],
    entry_point="agent1",
    max_handoffs=10,  # Prevent infinite loops
    repetitive_handoff_detection_window=5,  # Detect ping-pong
    repetitive_handoff_min_unique_agents=2
)
```

## Graph (Deterministic Workflows)

Structured workflows with defined execution paths:

```python
from strands import Agent
from strands.multiagent import GraphBuilder
from strands.multiagent.graph import GraphState
from strands.multiagent.base import Status

# Create agents
intake = Agent(name="intake", system_prompt="Classify and extract key information from requests.")
researcher = Agent(name="researcher", system_prompt="Research the topic thoroughly.")
reviewer = Agent(name="reviewer", system_prompt="Review for accuracy and completeness.")
writer = Agent(name="writer", system_prompt="Write the final polished output.")

# Build graph
builder = GraphBuilder()
builder.add_node(intake, "intake")
builder.add_node(researcher, "research")
builder.add_node(reviewer, "review")
builder.add_node(writer, "write")

# Define flow
builder.add_edge("intake", "research")
builder.add_edge("research", "review")
builder.add_edge("review", "write")

builder.set_entry_point("intake")
graph = builder.build()

result = graph("Create a comprehensive guide to machine learning")
```

### Conditional Routing

```python
def route_by_complexity(state: GraphState) -> bool:
    """Route complex requests to deep research."""
    intake_result = state.results.get("intake", {})
    output = str(intake_result.get("result", ""))
    return "complex" in output.lower()

def needs_revision(state: GraphState) -> bool:
    """Check if reviewer requested changes."""
    review_result = state.results.get("review", {})
    output = str(review_result.get("result", ""))
    return "revision needed" in output.lower()

builder.add_edge("intake", "deep_research", condition=route_by_complexity)
builder.add_edge("intake", "quick_research", condition=lambda s: not route_by_complexity(s))

# Feedback loop
builder.add_edge("review", "research", condition=needs_revision)
builder.add_edge("review", "write", condition=lambda s: not needs_revision(s))
```

### Parallel Execution

```python
# Fan-out pattern: one node feeds multiple parallel nodes
builder.add_node(coordinator, "coordinate")
builder.add_node(legal_reviewer, "legal")
builder.add_node(technical_reviewer, "technical")
builder.add_node(business_reviewer, "business")
builder.add_node(aggregator, "aggregate")

builder.add_edge("coordinate", "legal")
builder.add_edge("coordinate", "technical")
builder.add_edge("coordinate", "business")

# All converge to aggregator
builder.add_edge("legal", "aggregate")
builder.add_edge("technical", "aggregate")
builder.add_edge("business", "aggregate")
```

### Nested Graphs and Swarms

```python
from strands.multiagent import GraphBuilder, Swarm

# Create a swarm for research
research_swarm = Swarm([researcher1, researcher2, researcher3])

# Use swarm as a node in graph
builder = GraphBuilder()
builder.add_node(research_swarm, "research")  # Swarm as node
builder.add_node(writer, "write")
builder.add_edge("research", "write")
```

## Shared State Patterns

### Invocation State (Runtime Context)

Pass context that shouldn't appear in prompts:

```python
from strands import Agent, tool, ToolContext

@tool(context=True)
def personalized_search(query: str, tool_context: ToolContext) -> str:
    """Search with user context.
    
    Args:
        query: Search query
    """
    user_id = tool_context.invocation_state.get("user_id")
    preferences = tool_context.invocation_state.get("preferences", {})
    # Use context for personalized results
    return f"Results for {user_id}: {query}"

agent = Agent(tools=[personalized_search])
result = agent(
    "Find restaurants nearby",
    invocation_state={"user_id": "user-123", "preferences": {"cuisine": "italian"}}
)
```

### Graph Shared State

```python
# State flows through graph execution
result = graph("Process this request")

# Access state from results
for node_id, node_result in result.results.items():
    print(f"{node_id}: {node_result.status}")
    print(f"Output: {node_result.result}")
```

## Pattern Comparison

| Aspect | Agents as Tools | Swarm | Graph |
|--------|-----------------|-------|-------|
| Control | Orchestrator decides | Agents decide | Structure decides |
| Flow | Hierarchical | Emergent | Deterministic |
| Use case | Clear specialist roles | Exploration | Defined processes |
| Predictability | Medium | Low | High |
| Flexibility | High | Very high | Medium |

## Best Practices

1. **Clear agent roles**: Each agent should have a focused specialty
2. **Descriptive system prompts**: Help agents understand their responsibilities
3. **Tool docstrings**: Critical for agent tool selection
4. **Appropriate timeouts**: Set based on task complexity
5. **Error handling**: Implement fallbacks for agent failures
6. **Logging**: Enable debug logs for multi-agent debugging

```python
import logging
logging.getLogger("strands.multiagent").setLevel(logging.DEBUG)
```
