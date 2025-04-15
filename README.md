# Multi-Agent Bitcoin Trading Using CrewAI 

**IMPORTANT NOTE:** This project is created solely for academic research purposes and does not constitute financial investment advice. Do not use this project without conducting your own research.

A sophisticated AI-powered system for Bitcoin market analysis and trading decisions using CrewAI.


## 🚀 Overview

This project implements an automated Bitcoin trading analysis system that combines market research, technical analysis, and decision-making capabilities. The system uses CrewAI to coordinate multiple specialized agents that work together to provide comprehensive market insights and trading recommendations.

## ✨ Key Features

- **Multi-Agent System**: Coordinated team of specialized AI agents
- **Real-time Market Analysis**: Continuous monitoring of Bitcoin market conditions
- **Comprehensive Research**: News aggregation and sentiment analysis
- **Advanced Technical Analysis**: Multiple technical indicators and pattern recognition
- **Intelligent Decision Making**: AI-powered trading recommendations
- **Automated Reporting**: Detailed analysis reports in markdown format

## 🤖 System Architecture

### AI Agents

1. **Research Agent**
   - Market news collection and analysis
   - Sentiment analysis of market conditions
   - Regulatory updates monitoring
   - Institutional activity tracking

2. **Technical Analyst**
   - Price movement analysis
   - Technical indicators calculation
   - Support/resistance level identification
   - Market structure evaluation
   - Volume analysis
   - Trend analysis

3. **Decision Agent**
   - Research and technical analysis synthesis
   - Trading recommendations generation
   - Risk assessment
   - Entry/exit point suggestions
   - Position sizing recommendations

### Tools and Capabilities

- **Research Tools**
  - News scraping and aggregation
  - Sentiment analysis
  - Regulatory news tracking

- **Technical Tools**
  - Moving averages
  - RSI (Relative Strength Index)
  - MACD (Moving Average Convergence Divergence)
  - Bollinger Bands
  - Volume analysis
  - Pattern recognition

- **Analysis Tools**
  - Market trend analysis
  - Volatility measurement
  - Risk assessment
  - Position sizing calculations

## 🛠️ Installation

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/emirardagn/bitcointrading]
   cd bitcointrading
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -e .
   ```

4. **Configure Environment Variables**
   Create a `.env` file with necessary API keys and configurations:
   ```
   MODEL=gpt_model
   OPENAI_API_KEY=open_api_key
   BINANCE_API_KEY=binance_api_key
   BINANCE_SECRET_KEY=_binance_secret_key
   ```

## 📊 Usage

### Running the Analysis System

```bash
crewai run -m bitcointrading.main
```

### Output Reports

The system generates comprehensive reports in the `outputs` directory:
- `market_research.md`: Detailed market news and sentiment analysis
- `technical_analysis.md`: Technical indicators and price analysis
- `trading_decision.md`: Final trading recommendations and risk assessment

### Configuration

Customize agent behavior and analysis parameters in:
- `src/bitcointrading/config/agents.yaml`
- `src/bitcointrading/config/tasks.yaml`
- `src/bitcointrading/config/parameters.yaml`


## 📚 Dependencies

- Python 3.10+
- CrewAI
- pandas
- yfinance
- beautifulsoup4
- requests
- numpy
- scikit-learn
- matplotlib
- seaborn

## 📁 Project Structure

```
bitcointrading/
├── src/
│   └── bitcointrading/
│       ├── config/
│       │   ├── agents.yaml
│       │   ├── tasks.yaml
│       │   └── parameters.yaml
│       ├── tools/
│       │   ├── research_tools/
│       │   ├── technical_tools/
│       │   └── trading_tools/
│       ├── crew.py
│       └── main.py
├── outputs/
├── tests/
├── .env
├── pyproject.toml
└── README.md
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Contact

For questions, suggestions, or support:
- Email: [emirardagn@gmail.com]
- Email: [arda.gun.24752@ozu.edu.tr]

## 🙏 Acknowledgments

- CrewAI team for the amazing framework
- All contributors and supporters of the project
