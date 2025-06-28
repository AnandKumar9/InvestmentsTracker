import AnalyzerIndexFunds
import AnalyzerETFsStocks
import subprocess

if __name__ == '__main__':

    portflioHTMLPath = "/Users/anandkumar/Desktop/PortfolioHTML.txt"

    df1 = AnalyzerIndexFunds.extract_ticker_balances_from_html(portflioHTMLPath)

    for _, row in df1.iterrows():
        print(f"\t\t\"{row['Ticker']}\": \"{row['Current Balance']}\",")

    print()

    df2 = AnalyzerETFsStocks.extract_ticker_balances_from_html(portflioHTMLPath)
    for _, row in df2.iterrows():
        print(f"\t\t\"{row['Ticker']}\": \"{row['Current Balance']}\",")