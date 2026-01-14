#!/usr/bin/env python3
"""
Langfuse + Strands Telemetry Setup

Configures OpenTelemetry to send Strands agent traces to Langfuse.
Import and call setup_langfuse_telemetry() before creating any agents.

Environment variables required:
    LANGFUSE_PUBLIC_KEY: Your Langfuse public key (pk-lf-...)
    LANGFUSE_SECRET_KEY: Your Langfuse secret key (sk-lf-...)
    LANGFUSE_BASE_URL: Optional, defaults to https://cloud.langfuse.com

Usage:
    from setup_telemetry import setup_langfuse_telemetry
    setup_langfuse_telemetry()
    
    from strands import Agent
    agent = Agent(...)
"""

import os
import base64
from typing import Optional


def setup_langfuse_telemetry(
    public_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> "StrandsTelemetry":
    """
    Configure Langfuse OTEL exporter for Strands agents.
    
    Args:
        public_key: Langfuse public key. Falls back to LANGFUSE_PUBLIC_KEY env var.
        secret_key: Langfuse secret key. Falls back to LANGFUSE_SECRET_KEY env var.
        base_url: Langfuse host URL. Falls back to LANGFUSE_BASE_URL or default EU region.
    
    Returns:
        Configured StrandsTelemetry instance.
    
    Raises:
        ValueError: If credentials are not provided or found in environment.
    """
    # Get credentials from args or environment
    public_key = public_key or os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = secret_key or os.environ.get("LANGFUSE_SECRET_KEY")
    base_url = base_url or os.environ.get("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")
    
    if not public_key or not secret_key:
        raise ValueError(
            "Langfuse credentials required. Set LANGFUSE_PUBLIC_KEY and "
            "LANGFUSE_SECRET_KEY environment variables, or pass as arguments."
        )
    
    # Build Basic Auth header
    auth_string = f"{public_key}:{secret_key}"
    auth_encoded = base64.b64encode(auth_string.encode()).decode()
    
    # Configure OTEL exporter environment
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = f"{base_url}/api/public/otel"
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth_encoded}"
    
    # Initialize and return Strands telemetry
    from strands.telemetry import StrandsTelemetry
    telemetry = StrandsTelemetry()
    telemetry.setup_otlp_exporter()
    
    return telemetry


def create_traced_agent(
    model=None,
    system_prompt: str = "",
    tools: Optional[list] = None,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    tags: Optional[list] = None,
    **kwargs
) -> "Agent":
    """
    Create a Strands agent with Langfuse trace attributes pre-configured.
    
    Args:
        model: Strands model instance. If None, uses default BedrockModel.
        system_prompt: System prompt for the agent.
        tools: List of tools for the agent.
        session_id: Session ID for trace grouping.
        user_id: User ID for trace attribution.
        tags: List of tags for trace filtering.
        **kwargs: Additional arguments passed to Agent constructor.
    
    Returns:
        Configured Agent instance.
    """
    from strands import Agent
    
    # Build trace attributes
    trace_attributes = {}
    if session_id:
        trace_attributes["session.id"] = session_id
    if user_id:
        trace_attributes["user.id"] = user_id
    if tags:
        trace_attributes["langfuse.tags"] = tags
    
    # Use default model if not provided
    if model is None:
        from strands.models.bedrock import BedrockModel
        model = BedrockModel(model_id="us.anthropic.claude-sonnet-4-20250514-v1:0")
    
    return Agent(
        model=model,
        system_prompt=system_prompt,
        tools=tools or [],
        trace_attributes=trace_attributes if trace_attributes else None,
        **kwargs
    )


if __name__ == "__main__":
    # Quick test if run directly
    print("Testing Langfuse + Strands setup...")
    
    try:
        setup_langfuse_telemetry()
        print("✓ Telemetry configured successfully")
        
        agent = create_traced_agent(
            system_prompt="You are a helpful assistant.",
            session_id="test-session",
            tags=["test"]
        )
        print("✓ Agent created successfully")
        
        # Uncomment to test actual agent call:
        # result = agent("Say hello!")
        # print(f"✓ Agent response: {result}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
