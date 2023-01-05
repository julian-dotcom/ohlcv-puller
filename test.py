# =============================================================================
# IMPORTS
# =============================================================================

import requests
import pandas as pd
import ccxt
from pprint import pprint


BINANCE_SPOT = ccxt.binance()
BINANCE_FUTURE = ccxt.binance({"options": {"defaultType": "future"}})

old = [
    {"symbol": "1INCHBUSD", "category": "spot"},
    {"symbol": "AAVEBUSD", "category": "spot"},
    {"symbol": "ADABUSD", "category": "spot"},
    {"symbol": "ALGOBUSD", "category": "spot"},
    {"symbol": "APEBUSD", "category": "spot"},
    {"symbol": "ATOMBUSD", "category": "spot"},
    {"symbol": "AVAXBUSD", "category": "spot"},
    {"symbol": "BNBBUSD", "category": "spot"},
    {"symbol": "BTCBUSD", "category": "spot"},
    {"symbol": "COMPBUSD", "category": "spot"},
    {"symbol": "DOGEBUSD", "category": "spot"},
    {"symbol": "DOTBUSD", "category": "spot"},
    {"symbol": "ETCBUSD", "category": "spot"},
    {"symbol": "ETHBUSD", "category": "spot"},
    {"symbol": "FILBUSD", "category": "spot"},
    {"symbol": "LINKBUSD", "category": "spot"},
    {"symbol": "LTCBUSD", "category": "spot"},
    {"symbol": "MATICBUSD", "category": "spot"},
    {"symbol": "NEARBUSD", "category": "spot"},
    {"symbol": "QNTBUSD", "category": "spot"},
    {"symbol": "SHIBBUSD", "category": "spot"},
    {"symbol": "SOLBUSD", "category": "spot"},
    {"symbol": "SUSHIBUSD", "category": "spot"},
    {"symbol": "TRXBUSD", "category": "spot"},
    {"symbol": "UNIBUSD", "category": "spot"},
    {"symbol": "VETBUSD", "category": "spot"},
    {"symbol": "XLMBUSD", "category": "spot"},
    {"symbol": "XMRBUSD", "category": "spot"},
    {"symbol": "XRPBUSD", "category": "spot"},
    {"symbol": "BTCBUSD", "category": "futures"},
]


new_ = [
    {"symbol": "WBTCBUSD", "category": "spot"},
    {"symbol": "BCHBUSD", "category": "spot"},
    {"symbol": "LDOBUSD", "category": "spot"},
    {"symbol": "ICPBUSD", "category": "spot"},
    {"symbol": "EOSBUSD", "category": "spot"},
    {"symbol": "HBARBUSD", "category": "spot"},
    {"symbol": "LUNCBUSD", "category": "spot"},
    {"symbol": "EGLDBUSD", "category": "spot"},
    {"symbol": "FLOWBUSD", "category": "spot"},
    {"symbol": "THETABUSD", "category": "spot"},
    {"symbol": "XTZBUSD", "category": "spot"},
    {"symbol": "CHZBUSD", "category": "spot"},
    {"symbol": "AXSBUSD", "category": "spot"},
    {"symbol": "ZECBUSD", "category": "spot"},
    {"symbol": "SANDBUSD", "category": "spot"},
    {"symbol": "FTMBUSD", "category": "spot"},
    {"symbol": "TWTBUSD", "category": "spot"},
    {"symbol": "MANABUSD", "category": "spot"},
    {"symbol": "CAKEBUSD", "category": "spot"},
    {"symbol": "GRTBUSD", "category": "spot"},
    {"symbol": "MKRBUSD", "category": "spot"},
    {"symbol": "DASHBUSD", "category": "spot"},
    {"symbol": "PAXGBUSD", "category": "spot"},
    {"symbol": "IOTABUSD", "category": "spot"},
]
