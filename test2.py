top_50 = [
    "BTCBUSD",
    "ETHBUSD",
    "BNBBUSD",
    "XRPBUSD",
    "DOGEBUSD",
    "ADABUSD",
    "MATICBUSD",
    "LTCBUSD",
    "DOTBUSD",
    "TRXBUSD",
    "SOLBUSD",
    "SHIBBUSD",
    "UNIBUSD",
    "AVAXBUSD",
    "WBTCBUSD",
    "ATOMBUSD",
    "LINKBUSD",
    "XMRBUSD",
    "ETCBUSD",
    "BCHBUSD",
    "XLMBUSD",
    "APEBUSD",
    "QNTBUSD",
    "ALGOBUSD",
    "NEARBUSD",
    "FILBUSD",
    "VETBUSD",
    "LDOBUSD",
    "ICPBUSD",
    "EOSBUSD",
    "HBARBUSD",
    "LUNCBUSD",
    "EGLDBUSD",
    "AAVEBUSD",
    "FLOWBUSD",
    "THETABUSD",
    "XTZBUSD",
    "CHZBUSD",
    "AXSBUSD",
    "ZECBUSD",
    "SANDBUSD",
    "FTMBUSD",
    "TWTBUSD",
    "MANABUSD",
    "CAKEBUSD",
    "GRTBUSD",
    "MKRBUSD",
    "DASHBUSD",
    "PAXGBUSD",
    "IOTABUSD",
]


coins = [{"symbol": c, "category": "spot"} for c in top_50]

new_ = [
    {"symbol": "BTCBUSD", "category": "spot"},
    {"symbol": "ETHBUSD", "category": "spot"},
    {"symbol": "BNBBUSD", "category": "spot"},
    {"symbol": "XRPBUSD", "category": "spot"},
    {"symbol": "DOGEBUSD", "category": "spot"},
    {"symbol": "ADABUSD", "category": "spot"},
    {"symbol": "MATICBUSD", "category": "spot"},
    {"symbol": "LTCBUSD", "category": "spot"},
    {"symbol": "DOTBUSD", "category": "spot"},
    {"symbol": "TRXBUSD", "category": "spot"},
    {"symbol": "SOLBUSD", "category": "spot"},
    {"symbol": "SHIBBUSD", "category": "spot"},
    {"symbol": "UNIBUSD", "category": "spot"},
    {"symbol": "AVAXBUSD", "category": "spot"},
    {"symbol": "WBTCBUSD", "category": "spot"},
    {"symbol": "ATOMBUSD", "category": "spot"},
    {"symbol": "LINKBUSD", "category": "spot"},
    {"symbol": "XMRBUSD", "category": "spot"},
    {"symbol": "ETCBUSD", "category": "spot"},
    {"symbol": "BCHBUSD", "category": "spot"},
    {"symbol": "XLMBUSD", "category": "spot"},
    {"symbol": "APEBUSD", "category": "spot"},
    {"symbol": "QNTBUSD", "category": "spot"},
    {"symbol": "ALGOBUSD", "category": "spot"},
    {"symbol": "NEARBUSD", "category": "spot"},
    {"symbol": "FILBUSD", "category": "spot"},
    {"symbol": "VETBUSD", "category": "spot"},
    {"symbol": "LDOBUSD", "category": "spot"},
    {"symbol": "ICPBUSD", "category": "spot"},
    {"symbol": "EOSBUSD", "category": "spot"},
    {"symbol": "HBARBUSD", "category": "spot"},
    {"symbol": "LUNCBUSD", "category": "spot"},
    {"symbol": "EGLDBUSD", "category": "spot"},
    {"symbol": "AAVEBUSD", "category": "spot"},
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
old = [
    "1INCHBUSD",
    "AAVEBUSD",
    "ADABUSD",
    "ALGOBUSD",
    "APEBUSD",
    "ATOMBUSD",
    "AVAXBUSD",
    "BNBBUSD",
    "BTCBUSD",
    "COMPBUSD",
    "DOGEBUSD",
    "DOTBUSD",
    "ETCBUSD",
    "ETHBUSD",
    "FILBUSD",
    "LINKBUSD",
    "LTCBUSD",
    "MATICBUSD",
    "NEARBUSD",
    "QNTBUSD",
    "SHIBBUSD",
    "SOLBUSD",
    "SUSHIBUSD",
    "TRXBUSD",
    "UNIBUSD",
    "VETBUSD",
    "XLMBUSD",
    "XMRBUSD",
    "XRPBUSD",
]


print([n for n in new_ if n["symbol"] not in old])


filtered = [
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
