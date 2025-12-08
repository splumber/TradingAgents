# TradingAgents Examples

This directory contains example scripts demonstrating different use cases of TradingAgents.

## Available Examples

### local_llm_example.py

Demonstrates how to use TradingAgents with **local LLMs via Ollama** instead of cloud-based APIs.

**Features:**
- Complete local LLM setup
- No API costs for LLM inference
- Privacy-focused configuration
- Example with error handling and troubleshooting

**Prerequisites:**
1. Install Ollama from https://ollama.ai
2. Pull required models:
   ```bash
   ollama pull llama3.2
   ollama pull llama3.1
   ollama pull nomic-embed-text
   ```
3. Start Ollama server: `ollama serve`
4. Set Alpha Vantage API key: `export ALPHA_VANTAGE_API_KEY=your_key`

**Usage:**
```bash
cd examples
python local_llm_example.py
```

**See also:** [Local LLM Setup Guide](../docs/LOCAL_LLM_SETUP.md) for detailed instructions.

## Adding Your Own Examples

Feel free to contribute examples! Useful examples include:

- Different LLM provider configurations (Anthropic, Google, etc.)
- Custom analyst team configurations
- Backtesting strategies
- Portfolio management workflows
- Integration with trading platforms

To contribute, create a new Python file in this directory with:
1. Clear documentation at the top
2. Error handling
3. Example output
4. Prerequisites listed
