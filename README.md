# Agente telegram de Analise Financeira

Um bot inteligente para Telegram que atua como um **Analista Financeiro Sênior**, utilizando IA + análise técnica para avaliar ações.

O bot combina dados de mercado em tempo real com indicadores técnicos para gerar análises completas e sinais de trading.

---

## 🚀 Funcionalidades

- 📊 Consulta de dados históricos de ações (via Yahoo Finance)
- 📈 Indicadores técnicos:
  - SMA (Média Móvel Simples)
  - EMA (Média Móvel Exponencial)
  - RSI (Índice de Força Relativa)
  - MACD
  - Bollinger Bands
  - Volatilidade
  - ATR
- 📉 Detecção de tendência de mercado
- 🔎 Análise de volume
- 🧠 Detecção de regime de mercado (Bull / Bear / Sideways)
- 📰 Análise de notícias e sentimento
- 💡 Geração automática de sinais:
  - COMPRA
  - VENDA
  - AGUARDAR

---

## 🧠 Como funciona

O projeto utiliza:

- **LangChain** para criação de agentes inteligentes
- **OpenAI (GPT)** para raciocínio e geração de respostas
- **yfinance** para dados de mercado
- **Telegram Bot API** para interação com o usuário

Fluxo:

1. Usuário envia mensagem no Telegram  
2. O agente interpreta a intenção  
3. Busca dados reais da ação  
4. Aplica indicadores técnicos  
5. Gera uma análise estruturada + sinal de trading  
