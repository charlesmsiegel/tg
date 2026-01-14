# Model Providers Reference

Complete configuration guide for all supported model providers.

## Installation

Most providers require optional dependencies:

```bash
pip install 'strands-agents[anthropic]'   # Anthropic
pip install 'strands-agents[openai]'      # OpenAI
pip install 'strands-agents[ollama]'      # Ollama
pip install 'strands-agents[gemini]'      # Google Gemini
pip install 'strands-agents[litellm]'     # LiteLLM
pip install 'strands-agents[llamaapi]'    # LlamaAPI
pip install 'strands-agents[mistral]'     # Mistral
pip install 'strands-agents[sagemaker]'   # SageMaker
```

## Amazon Bedrock (Default)

No extra installation needed. Requires AWS credentials and model access enabled.

```python
from strands import Agent
from strands.models import BedrockModel

# Default (Claude 4 Sonnet in us-west-2)
agent = Agent()

# Explicit configuration
bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    temperature=0.3,
    top_p=0.8,
    region_name="us-west-2",
    streaming=True
)
agent = Agent(model=bedrock_model)

# Amazon Nova
agent = Agent(model=BedrockModel(model_id="us.amazon.nova-pro-v1:0"))
```

**Setup**: `aws configure` or set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`. Enable model access in Bedrock console.

## Anthropic API

```python
from strands import Agent
from strands.models.anthropic import AnthropicModel

model = AnthropicModel(
    client_args={
        "api_key": "<KEY>",  # Or set ANTHROPIC_API_KEY env var
    },
    model_id="claude-sonnet-4-20250514",
    max_tokens=1028,
    params={
        "temperature": 0.5,
    }
)
agent = Agent(model=model)
```

## OpenAI

```python
from strands import Agent
from strands.models.openai import OpenAIModel

model = OpenAIModel(
    client_args={
        "api_key": "<KEY>",  # Or set OPENAI_API_KEY env var
    },
    model_id="gpt-4o",
    params={
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)
agent = Agent(model=model)
```

## Ollama (Local)

```python
from strands import Agent
from strands.models.ollama import OllamaModel

model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1",
    temperature=0.7,
    keep_alive="10m",
    options={"top_k": 40}
)
agent = Agent(model=model)
```

**Setup**: Install Ollama from ollama.ai, then `ollama pull llama3.1`.

## llama.cpp (Local Server)

Connects to a running llama.cpp server (not a model file directly).

```python
from strands import Agent
from strands.models.llamacpp import LlamaCppModel

model = LlamaCppModel(
    base_url="http://localhost:8080",
    model_id="default",
    params={
        "temperature": 0.7,
        "max_tokens": 1000,
        "repeat_penalty": 1.1,
    }
)
agent = Agent(model=model)
```

**Setup**:
```bash
# Download a GGUF model
hf download ggml-org/Qwen3-4B-GGUF Qwen3-4B-Q4_K_M.gguf --local-dir ./models

# Start llama.cpp server
llama-server -m models/Qwen3-4B-Q4_K_M.gguf --host 0.0.0.0 --port 8080
```

## Google Gemini

```python
from strands import Agent
from strands.models.gemini import GeminiModel

model = GeminiModel(
    client_args={
        "api_key": "<KEY>",  # Or set GOOGLE_API_KEY env var
    },
    model_id="gemini-2.5-flash",
    params={"temperature": 0.7}
)
agent = Agent(model=model)
```

## LlamaAPI

```python
from strands import Agent
from strands.models.llamaapi import LlamaAPIModel

model = LlamaAPIModel(
    client_args={
        "api_key": "<KEY>",
    },
    model_id="Llama-4-Maverick-17B-128E-Instruct-FP8",
)
agent = Agent(model=model)
```

## LiteLLM (Universal Gateway)

Access 100+ models through unified interface:

```python
from strands import Agent
from strands.models.litellm import LiteLLMModel

# OpenAI via LiteLLM
agent = Agent(model=LiteLLMModel(model_id="gpt-4o"))

# Azure OpenAI
agent = Agent(model=LiteLLMModel(model_id="azure/gpt-4"))

# Any LiteLLM-supported model
agent = Agent(model=LiteLLMModel(model_id="together_ai/llama-3-70b"))
```

## Mistral AI

```python
from strands import Agent
from strands.models.mistral import MistralModel

model = MistralModel(
    api_key="<KEY>",
    model_id="mistral-large-latest",
)
agent = Agent(model=model)
```

## AWS SageMaker

```python
from strands import Agent
from strands.models.sagemaker import SageMakerModel

model = SageMakerModel(
    endpoint_name="your-endpoint-name",
    region_name="us-west-2"
)
agent = Agent(model=model)
```

## Runtime Configuration Updates

All models support runtime configuration updates:

```python
model = OllamaModel(host="http://localhost:11434", model_id="llama3.1")
model.update_config(temperature=0.9, top_p=0.8)
```

## Model Selection Guide

| Use Case | Recommended |
|----------|-------------|
| Production with AWS | Amazon Bedrock (Claude, Nova) |
| Best reasoning | Claude Sonnet 4, GPT-4o |
| Local development | Ollama (llama3.1) or llama.cpp |
| Cost-sensitive | Amazon Nova Lite, GPT-4o-mini |
| Multi-modal | Claude, GPT-4o, Gemini |
| Maximum flexibility | LiteLLM |
