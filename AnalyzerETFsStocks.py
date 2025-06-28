from bs4 import BeautifulSoup
from decimal import Decimal
import pandas as pd
import re

etfTickers = ["VGK", "VGT", "VOO", "VTI", "VUG"]
stockTickers = ["AAPL", "AMZN", "AVGO", "COF", "CVX", "GOOGL",
                "MSFT", "NVDA", "TSLA", "TSM", "UNH", "XOM"]
etfStockTickers = etfTickers + stockTickers

tickersToPrependWithEqualSign = ["VGK", "VTI", "COF"]

# Helper to extract dollar amounts from text
def extract_dollar_amounts(text):
    matches = re.findall(r"\$\s?([\d,]+\.\d{2})", text)
    return [Decimal(m.replace(",", "")) for m in matches]

# Main function to extract balances from an HTML file
def extract_ticker_balances_from_html(html_path):
    with open(html_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")
    results = {}

    for row in soup.find_all("tr"):
        row_text = row.get_text()
        for ticker in etfStockTickers:
            if ticker in row_text:
                amounts = extract_dollar_amounts(row_text)
                if amounts:
                    max_amount = max(amounts)
                    if ticker not in results or max_amount > results[ticker]:
                        results[ticker] = max_amount

    # df = pd.DataFrame([
    #     {
    #         "Ticker": ticker,
    #         "Current Balance": f"{results.get(ticker):.2f}" if ticker in results else ""
    #     }
    #     for ticker in etfStockTickers
    # ])

    df = pd.DataFrame([
        {
            "Ticker": ticker,
            "Current Balance": (
                f"={results[ticker]:.2f}" if ticker in tickersToPrependWithEqualSign else f"{results[ticker]:.2f}"
            ) if ticker in results else ""
        }
        for ticker in etfStockTickers
    ])

    return df

if __name__ == "__main__":
    import sys
    portfolioHTMLPath = sys.argv[1] if len(sys.argv) > 1 else "/Users/anandkumar/Desktop/PortfolioHTML.txt"
    df = extract_ticker_balances_from_html(portfolioHTMLPath)
    for _, row in df.iterrows():
        print(f"\t\t\"{row['Ticker']}\": \"{row['Current Balance']}\",")