import pandas as pd
import yfinance as yf
from tabulate import tabulate

# Official Nifty 50 list (static)
nifty50 = [
    "RELIANCE","TCS","HDFCBANK","ICICIBANK","INFY","ITC","LT","SBIN",
    "HINDUNILVR","BHARTIARTL","KOTAKBANK","AXISBANK","BAJFINANCE",
    "ASIANPAINT","MARUTI","SUNPHARMA","TITAN","ULTRACEMCO","ONGC",
    "NTPC","POWERGRID","M&M","WIPRO","NESTLEIND","HCLTECH","TECHM",
    "BAJAJFINSV","COALINDIA","TATAMOTORS","INDUSINDBK","JSWSTEEL",
    "GRASIM","ADANIPORTS","CIPLA","DRREDDY","EICHERMOT","BRITANNIA",
    "HEROMOTOCO","SHREECEM","TATASTEEL","BPCL","DIVISLAB",
    "APOLLOHOSP","HDFCLIFE","SBILIFE","BAJAJ-AUTO",
    "UPL","TATACONSUM","ADANIENT","LTIM"
]

results = []

for symbol in nifty50:
    try:
        df = yf.download(symbol + ".NS", period="2mo", progress=False)

        if len(df) < 30:
            continue

        df["EMA9"] = df["Close"].ewm(span=9, adjust=False).mean()
        df["EMA26"] = df["Close"].ewm(span=26, adjust=False).mean()

        df["Signal"] = df["EMA9"] > df["EMA26"]
        df["Crossover"] = df["Signal"].astype(int).diff()

        if 1 in df.tail(5)["Crossover"].values:
            ticker = yf.Ticker(symbol + ".NS")
            sector = ticker.info.get("sector", "Unknown")

            results.append({
                "Stock": symbol,
                "Sector": sector
            })

    except Exception:
        pass

if results:
    df_result = pd.DataFrame(results).sort_values("Sector")
    print("\n📊 9 EMA / 26 EMA Bullish Crossovers (Last Week)\n")
    print(tabulate(df_result, headers="keys", tablefmt="grid"))
else:
    print("No crossovers found in last week.")