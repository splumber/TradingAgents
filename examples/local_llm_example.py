"""
Example script demonstrating how to use TradingAgents with local LLMs via Ollama.

This script shows how to configure TradingAgents to use local Ollama models
instead of cloud-based APIs like OpenAI.

Prerequisites:
1. Install Ollama: https://ollama.ai
2. Pull required models:
   ollama pull llama3.2
   ollama pull llama3.1
   ollama pull nomic-embed-text
3. Start Ollama: ollama serve
4. Set Alpha Vantage API key (still needed for market data):
   export ALPHA_VANTAGE_API_KEY=your_key_here
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

def main():
    # Configure for local Ollama
    config = DEFAULT_CONFIG.copy()
    
    # Set provider to Ollama
    config["llm_provider"] = "ollama"
    config["backend_url"] = "http://localhost:11434/v1"
    
    # Configure local models
    # Use smaller/faster model for quick thinking
    config["quick_think_llm"] = "llama3.2"
    # Use more capable model for deep thinking
    config["deep_think_llm"] = "llama3.1"
    
    # Optional: Adjust debate rounds for faster execution
    # (more rounds = more thorough but slower analysis)
    config["max_debate_rounds"] = 1
    config["max_risk_discuss_rounds"] = 1
    
    # Initialize TradingAgents with local LLM configuration
    print("Initializing TradingAgents with local LLMs via Ollama...")
    print(f"Quick thinking model: {config['quick_think_llm']}")
    print(f"Deep thinking model: {config['deep_think_llm']}")
    print(f"Backend URL: {config['backend_url']}")
    print()
    
    try:
        ta = TradingAgentsGraph(debug=True, config=config)
        
        # Example: Analyze NVDA stock on a specific date
        ticker = "NVDA"
        date = "2024-05-10"
        
        print(f"Running analysis for {ticker} on {date}...")
        print("This may take several minutes with local models...")
        print()
        
        # Run the analysis
        final_state, decision = ta.propagate(ticker, date)
        
        # Display results
        print("\n" + "="*80)
        print("ANALYSIS COMPLETE")
        print("="*80)
        print(f"\nFinal Trading Decision for {ticker} on {date}:")
        print(decision)
        print("\n" + "="*80)
        
        # You can also access detailed reports
        if final_state.get("market_report"):
            print("\nMarket Analysis Summary:")
            print(final_state["market_report"][:500] + "...")
        
        if final_state.get("final_trade_decision"):
            print("\nPortfolio Manager Decision:")
            print(final_state["final_trade_decision"])
        
    except Exception as e:
        print(f"\nError: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Verify models are installed: ollama list")
        print("3. Pull missing models:")
        print("   ollama pull llama3.2")
        print("   ollama pull llama3.1")
        print("   ollama pull nomic-embed-text")
        print("4. Check Alpha Vantage API key is set")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
