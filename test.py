import ccxt
from pprint import pprint

tokens = [
    "BTC",
    "ETH",
    "BNB",
    "XRP",
    "DOGE",
    "ADA",
    "MATIC",
    "DOT",
    "LTC",
    "SHIB",
    "OKB",
    "SOL",
    "TRX",
    "UNI",
    "AVAX",
    "LEO",
    "LINK",
    "ATOM",
    "TON",
    "XMR",
    "ETC",
    "XLM",
    "QNT",
    "CRO",
    "ALGO",
    "FIL",
    "APE",
    "NEAR",
    "VET",
]
BINANCE = ccxt.binance()
res = BINANCE.fetchMarkets()
symbols = [r["symbol"] for r in res if "USD" in r["symbol"]]
symbols = [s for s in symbols if s.split("/")[0] in tokens]
symbols = [s.split("/") for s in symbols]
filtered = []

for token in tokens:
    temp = ["/".join(s) for s in symbols if token in s]
    if f"{token}/BUSD" in temp:
        filtered.append(f"{token}/BUSD")
    elif f"{token}/USDT" in temp:
        filtered.append(f"{token}/USDT")
    else:
        print(f"Warning: Neither USDT nor BUSD for {token}")

filtered = ["".join(f.split("/")) for f in filtered]

pprint((sorted(filtered)))
