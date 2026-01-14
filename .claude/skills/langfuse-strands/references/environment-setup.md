# Environment Setup Reference

## Required Environment Variables

### Langfuse Configuration

```bash
# Langfuse API credentials (from project settings)
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."

# Langfuse host (choose one)
export LANGFUSE_BASE_URL="https://cloud.langfuse.com"      # EU region (default)
export LANGFUSE_BASE_URL="https://us.cloud.langfuse.com"   # US region
export LANGFUSE_BASE_URL="http://localhost:3000"            # Self-hosted
```

### OpenTelemetry Exporter Configuration

These are auto-configured when using the setup pattern in SKILL.md, but can be set manually:

```bash
# OTEL endpoint (Langfuse's OTEL ingestion)
export OTEL_EXPORTER_OTLP_ENDPOINT="https://cloud.langfuse.com/api/public/otel"

# Authorization header (base64 encoded public:secret)
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Basic <base64_encoded_credentials>"
```

### AWS Configuration (for Bedrock)

```bash
# AWS credentials
export AWS_ACCESS_KEY_ID="..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_SESSION_TOKEN="..."  # If using temporary credentials

# Default region for Bedrock
export AWS_DEFAULT_REGION="us-east-1"
# or
export AWS_REGION="us-east-1"
```

### Alternative Model Provider Credentials

```bash
# Anthropic direct API
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI
export OPENAI_API_KEY="sk-..."

# Ollama (local)
export OLLAMA_HOST="http://localhost:11434"
```

## Python Setup Helper

Create a `setup_telemetry.py` module for reuse:

```python
import os
import base64

def setup_langfuse_telemetry():
    """Configure Langfuse OTEL exporter. Call before creating agents."""
    
    # Validate required vars
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    base_url = os.environ.get("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")
    
    if not public_key or not secret_key:
        raise ValueError("LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY must be set")
    
    # Build auth header
    auth = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
    
    # Configure OTEL
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = f"{base_url}/api/public/otel"
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth}"
    
    # Initialize Strands telemetry
    from strands.telemetry import StrandsTelemetry
    return StrandsTelemetry().setup_otlp_exporter()
```

Usage:
```python
from setup_telemetry import setup_langfuse_telemetry

# Call once at startup
setup_langfuse_telemetry()

# Then create agents as normal
from strands import Agent
agent = Agent(...)
```

## .env File Template

```env
# Langfuse
LANGFUSE_PUBLIC_KEY=pk-lf-your-key
LANGFUSE_SECRET_KEY=sk-lf-your-secret
LANGFUSE_BASE_URL=https://cloud.langfuse.com

# AWS (for Bedrock)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_DEFAULT_REGION=us-east-1

# Optional: Alternative providers
# ANTHROPIC_API_KEY=sk-ant-...
# OPENAI_API_KEY=sk-...
```

Load with python-dotenv:
```python
from dotenv import load_dotenv
load_dotenv()

# Then setup telemetry
from setup_telemetry import setup_langfuse_telemetry
setup_langfuse_telemetry()
```

## Bedrock Model Access

Before using Bedrock models, enable access in AWS Console:

1. Go to Amazon Bedrock console
2. Navigate to "Model access" in left sidebar  
3. Click "Manage model access"
4. Enable the models you need (e.g., Claude Sonnet 4)
5. Wait for access status to show "Access granted"

Common model IDs:
- `us.anthropic.claude-sonnet-4-20250514-v1:0` - Claude Sonnet 4
- `us.anthropic.claude-3-5-sonnet-20241022-v2:0` - Claude 3.5 Sonnet
- `us.amazon.nova-premier-v1:0` - Amazon Nova Premier
- `us.amazon.nova-micro-v1:0` - Amazon Nova Micro
