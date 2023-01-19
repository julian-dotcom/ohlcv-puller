import requests
import pandas as pd
import time

date = 1674086400 * 1000
interval = "1m"
symbol = "SOLBUSD"
headers = ["timestamp", "open", "high", "low", "close", "volume"]
data = []
while date < 1674165600000:
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&startTime={date}&limit={1400}"
    res = requests.get(url)
    res = [d[0:6] for d in res.json()]
    if len(data) > 0 and data[-1][0] == res[-1][0]:
        break

    data += res
    date = res[-1][0]
    # print(date)
    time.sleep(1)


df = pd.DataFrame(data, columns=headers)
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
df = df[["timestamp", "close"]]
print(df)
df.to_csv("sol-data.csv", index=False)
