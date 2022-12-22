# =============================================================================
# IMPORTS
# =============================================================================

import requests
import pandas as pd
import ccxt
from pprint import pprint


BINANCE_SPOT = ccxt.binance()
BINANCE_FUTURE = ccxt.binance({"options": {"defaultType": "future"}})
URL = "https://fapi.binance.com" + "/fapi/v1/klines"
START = 1671616800000

res = BINANCE_SPOT.fetchOHLCV(symbol="BTCBUSD", timeframe="1m", limit=5, since=START)
res2 = BINANCE_FUTURE.fetchOHLCV(symbol="BTCBUSD", timeframe="1m", limit=5, since=START)
res3 = requests.get(
    URL + f"?symbol={'BTCBUSD'}&interval={'1m'}&limit={5}&startTime={START}"
).json()


res = pd.DataFrame(res)
res[0] = pd.to_datetime(res[0], unit="ms")

res2 = pd.DataFrame(res2)
res2[0] = pd.to_datetime(res2[0], unit="ms")

res3 = pd.DataFrame(res3)
res3[0] = pd.to_datetime(res3[0], unit="ms")


pprint(res)
pprint(res2)
pprint(res3)
