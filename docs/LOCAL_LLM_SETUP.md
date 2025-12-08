# Local LLM Setup Guide

TradingAgents supports running entirely on **local LLMs** using [Ollama](https://ollama.ai), which allows you to run models locally without any API costs or internet dependency for LLM inference.

## Why Use Local LLMs?

- **No API Costs**: Run unlimited inference without paying per-token fees
- **Privacy**: Your trading data and analysis stays on your machine
- **No Rate Limits**: No throttling or rate limiting
- **Offline Capability**: Run without internet connection (except for market data APIs)

## Prerequisites

### 1. Install Ollama

Install Ollama from the official website: [https://ollama.ai](https://ollama.ai)

**Installation options:**
- **macOS/Windows**: Download and run the installer
- **Linux**: 
  ```bash
  curl -fsSL https://ollama.ai/install.sh | sh
  ```

### 2. Pull Required Models

After installing Ollama, pull the models you want to use:

```bash
# For quick thinking (recommended: smaller, faster models)
ollama pull llama3.2      # ~2GB - Fast and efficient
ollama pull llama3.1:8b   # ~4.7GB - Good balance

# For deep thinking (recommended: larger, more capable models)  
ollama pull llama3.1      # ~4.7GB - Default 8B parameter model
ollama pull llama3.1:70b  # ~40GB - Most capable (requires powerful GPU)
ollama pull qwen3         # ~4.7GB - Good alternative

# For embeddings (REQUIRED for memory system)
ollama pull nomic-embed-text  # ~274MB - Embeddings for memory
```

**Model Recommendations:**
- **Minimum Setup** (8GB+ RAM): llama3.2 + llama3.1:8b + nomic-embed-text
- **Recommended Setup** (16GB+ RAM, GPU): llama3.1:8b + qwen3 + nomic-embed-text
- **High-Performance Setup** (32GB+ RAM, Strong GPU): llama3.1:70b + llama3.1:70b + nomic-embed-text

### 3. Start Ollama Server

Ollama usually starts automatically after installation. If not, start it manually:

```bash
ollama serve
```

Verify it's running by opening http://localhost:11434 in your browser.

### 4. Alpha Vantage API (Still Required)

You still need Alpha Vantage API for market data since local LLMs cannot fetch real-time market data:

```bash
export ALPHA_VANTAGE_API_KEY=$YOUR_ALPHA_VANTAGE_API_KEY
```

Get a free API key from: [https://www.alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key)

## Using Local LLMs with TradingAgents

### Option 1: CLI (Interactive)

Run the CLI and select Ollama when prompted:

```bash
python -m cli.main
```

When prompted:
1. **LLM Provider**: Select "Ollama"
2. **Backend URL**: http://localhost:11434/v1 (default)
3. **Quick-Thinking LLM**: Select "llama3.2" or "llama3.1"
4. **Deep-Thinking LLM**: Select "llama3.1" or "qwen3"

### Option 2: Python API (Programmatic)

Use the Python API with local LLMs:

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# Configure for local Ollama
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "ollama"
config["backend_url"] = "http://localhost:11434/v1"
config["quick_think_llm"] = "llama3.2"  # Fast local model
config["deep_think_llm"] = "llama3.1"   # More capable local model

# Optional: Adjust debate rounds for performance
config["max_debate_rounds"] = 1  # Reduce for faster execution
config["max_risk_discuss_rounds"] = 1

# Initialize with local LLM config
ta = TradingAgentsGraph(debug=True, config=config)

# Run analysis
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

## Performance Considerations

### Hardware Requirements

**Minimum:**
- CPU: Modern multi-core processor
- RAM: 8GB (for 7B parameter models)
- Storage: 10GB+ free space

**Recommended:**
- CPU: Modern 8+ core processor
- RAM: 16GB+
- GPU: NVIDIA GPU with 8GB+ VRAM (for significantly faster inference)
- Storage: 50GB+ free space

**High-Performance:**
- CPU: High-end multi-core processor
- RAM: 32GB+
- GPU: NVIDIA GPU with 24GB+ VRAM (for 70B models)
- Storage: 100GB+ free space

### GPU Acceleration

Ollama automatically uses GPU if available. To verify GPU usage:

```bash
ollama ps
```

If you have an NVIDIA GPU, ensure you have CUDA drivers installed.

### Performance Tips

1. **Use Smaller Models for Quick Thinking**: Use llama3.2 or llama3.1:8b for the quick_think_llm
2. **Reduce Debate Rounds**: Set `max_debate_rounds` and `max_risk_discuss_rounds` to 1
3. **Keep Models in Memory**: Don't shut down Ollama between runs to keep models loaded
4. **Monitor Resources**: Use `ollama ps` to see running models and resource usage

## Automatic Features with Local LLMs

When using Ollama, TradingAgents automatically:

1. **Uses Local Embeddings**: Switches to `nomic-embed-text` for the memory system
2. **Adjusts API Calls**: Uses OpenAI-compatible API format that Ollama supports
3. **Handles Errors Gracefully**: Falls back to simpler operations if models are unavailable

## Troubleshooting

### Ollama Not Running
```bash
# Check if Ollama is running
curl http://localhost:11434

# Start Ollama manually
ollama serve
```

### Model Not Found
```bash
# List available models
ollama list

# Pull missing model
ollama pull llama3.1
```

### Out of Memory
- Use smaller models (e.g., llama3.2 instead of llama3.1:70b)
- Reduce debate rounds in config
- Close other applications
- Consider using a machine with more RAM

### Slow Performance
- Ensure GPU is being used: `ollama ps`
- Use smaller models for quick thinking
- Keep models loaded between runs
- Reduce debate rounds

### Connection Errors
- Verify Ollama is running on port 11434
- Check firewall settings
- Ensure backend_url is set to "http://localhost:11434/v1"

## Limitations

- **Performance**: Local models are slower than cloud APIs, especially without GPU
- **Model Quality**: Open-source models may not match GPT-4 or Claude in quality
- **Resource Intensive**: Requires significant RAM and compute resources
- **Market Data**: Still requires internet connection for Alpha Vantage API

## Mixed Setup (Advanced)

You can mix local and cloud providers:

```python
# Use local LLMs for inference, but cloud for embeddings (if preferred)
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "ollama"
config["backend_url"] = "http://localhost:11434/v1"
config["quick_think_llm"] = "llama3.2"
config["deep_think_llm"] = "llama3.1"

# Note: Memory system will auto-detect Ollama and use nomic-embed-text
# To use cloud embeddings instead, you'd need to modify the memory.py
```

## Supported LLM Providers

TradingAgents supports multiple providers:

- **OpenAI**: GPT-4, GPT-4o, o1, etc.
- **Anthropic**: Claude Sonnet, Claude Opus
- **Google**: Gemini 2.0, Gemini 2.5
- **OpenRouter**: Access to multiple models
- **Ollama**: Local models (llama3, qwen, etc.)

## Getting Help

If you encounter issues:

1. Check Ollama documentation: [https://github.com/ollama/ollama](https://github.com/ollama/ollama)
2. Verify models are downloaded: `ollama list`
3. Check Ollama logs for errors
4. Open an issue on the TradingAgents GitHub repository

## Example: Complete Local Setup

```bash
# 1. Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Pull models
ollama pull llama3.2
ollama pull llama3.1
ollama pull nomic-embed-text

# 3. Start Ollama
ollama serve &

# 4. Set Alpha Vantage API key
export ALPHA_VANTAGE_API_KEY=your_key_here

# 5. Run TradingAgents
cd TradingAgents
python -m cli.main
# Select Ollama, llama3.2, and llama3.1 when prompted
```
