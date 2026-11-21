# Stock Market Analyser

A Python web application for exploring Indian equity market data and visualizing stock performance.

## Project overview
The inspected application uses Flask to serve a dashboard and yfinance to retrieve market information. Matplotlib is used to generate stock-range visualizations, including sector-oriented groups.

## Technology stack
- Python and Flask
- yfinance
- NumPy
- Matplotlib

## Run locally
1. Clone the repository.
2. Install dependencies from `requirements.txt` if present:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the application using its Flask entry point (inspect the repository for the exact filename).
4. Open the local URL printed by Flask.

## Engineering notes
Market-data provider responses can be incomplete or unavailable. Validate each quote before using it, avoid repeated requests for the same ticker, add caching and timeouts, and distinguish missing data from zero values. Do not run Flask debug mode in a public deployment.

## Future improvements
- Move ticker universes and sector mappings into configuration files.
- Add provider abstraction, caching and retry policies.
- Add tests for missing prices and 52-week range calculations.
- Add structured logging, responsive tables and CI checks.

## Disclaimer
This project is for market-data exploration and education, not investment advice.
