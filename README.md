# Bitcoin Trading Analysis System

A sophisticated AI-powered system for Bitcoin market analysis and trading decisions using CrewAI.

## Overview

This project implements an automated Bitcoin trading analysis system that combines market research, technical analysis, and decision-making capabilities. The system uses CrewAI to coordinate multiple specialized agents that work together to provide comprehensive market insights and trading recommendations.

## Features

- **Market Research Agent**: Scrapes and analyzes Bitcoin market news and sentiment
- **Technical Analysis Agent**: Performs detailed technical analysis using various indicators
- **Decision Agent**: Synthesizes research and technical analysis to make trading recommendations

## System Components

### Agents

1. **Research Agent**
   - Collects market news and developments
   - Analyzes market sentiment
   - Tracks regulatory updates
   - Monitors institutional activity

2. **Technical Analyst**
   - Analyzes price movements
   - Calculates technical indicators
   - Identifies support/resistance levels
   - Evaluates market structure

3. **Decision Agent**
   - Synthesizes research and technical analysis
   - Makes trading recommendations
   - Provides risk assessment
   - Suggests entry/exit points

### Tools

- **Research Tools**: News scraping and sentiment analysis
- **Technical Tools**: Various technical indicators and analysis tools

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd bitcointrading
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

## Usage

To run the Bitcoin trading analysis system:

```bash
python -m bitcointrading.main
```

The system will:
1. Collect and analyze market data
2. Perform technical analysis
3. Generate trading recommendations
4. Save reports in the `outputs` directory

## Outputs

The system generates three main reports:
- `market_research.md`: Market news and sentiment analysis
- `technical_analysis.md`: Technical indicators and price analysis
- `trading_decision.md`: Final trading recommendations

## Dependencies

- Python 3.10+
- CrewAI
- pandas
- yfinance
- beautifulsoup4
- requests
- numpy

## Project Structure

```
bitcointrading/
├── src/
│   └── bitcointrading/
│       ├── config/
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       ├── tools/
│       │   ├── research_tools/
│       │   └── technical_tools/
│       ├── crew.py
│       └── main.py
├── outputs/
├── tests/
└── pyproject.toml
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Your chosen license]

## Contact

For questions or support, please contact [your contact information]
