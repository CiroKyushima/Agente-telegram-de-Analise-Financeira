from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain import hub
from .tools import *
from settings import settings

def ask_agent(question: str):
    llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model=settings.MODEL_NAME, temperature=0)
    tools = [get_stock_data,
            calculate_sma,
            calculate_ema,
            calculate_rsi,
            calculate_macd,
            calculate_bollinger_bands,
            calculate_volatility,
            detect_trend,
            generate_trading_signal,
            calculate_sharpe_ratio,
            calculate_max_drawdown,
            calculate_atr,
            analyze_volume_trend,
            detect_market_regime,
            analyze_market_news]
    
    base_prompt = hub.pull("hwchase17/openai-tools-agent")
    
    instructions = """Você é um Analista Financeiro Sênior especializado em B3 e NASDAQ.
    Ao ser questionado se 'vale a pena' comprar ou vender:
    1. Sempre busque dados atuais com 'fetch_stock_data'.
    2. Sempre valide a tendência com 'technical_analysis_indicator'.
    3. Apresente os números principais em uma tabela Markdown simples.
    4. Conclua com uma análise técnica (ex: 'Preço acima da média móvel, indicando força').
    5. Adicione um aviso legal de que isso não é recomendação de investimento."""
    
    prompt = base_prompt.partial(instructions=instructions)
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    result = agent_executor.invoke({"input": question})
    return result["output"]
