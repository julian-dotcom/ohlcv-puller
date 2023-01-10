# =============================================================================
# IMPORTS
# =============================================================================
import sys, os, pytz, time, traceback
import boto3
import datetime as dt
from dotenv import load_dotenv
import pandas as pd
import ccxt
from pprint import pprint
from io import StringIO

load_dotenv()
# =============================================================================
# CONFIG
# =============================================================================
BINANCE_SPOT = ccxt.binance()
BINANCE_FUTURES = ccxt.binance({"options": {"defaultType": "future"}})
BUCKET_NAME = "binance-ohlcv"
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name="eu-central-1",
)

# =============================================================================
# OBJECT
# =============================================================================
class OhlcvPuller:
    HEADER = ["timestamp", "open", "high", "low", "close", "volume"]
    MINUTES_PER_DAY = 24 * 60
    MAX_EXCEPTIONS = 100

    def __init__(self, coins, timeframe, start_str=None, end_str=None):
        self.coins = coins
        self.timeframe = timeframe
        self.determine_start_n_end_time(start_str, end_str)
        self.create_list_of_all_midnights()

    # =============================================================================
    # MAIN
    # =============================================================================
    def main(self):
        print("Sleeping 10 seconds for crontab...")
        time.sleep(10)
        for coin in self.coins:
            self.get_ohlcv_for_coin_for_all_dates(coin)

    # =============================================================================
    # Iterate over all dates, fetch for every single date
    # =============================================================================
    def get_ohlcv_for_coin_for_all_dates(self, coin):
        symbol, cat = coin["symbol"], coin["category"]
        for i in range(len(self.midnights) - 1):
            print(coin)
            cur_midnight, next_midnight = self.midnights[i], self.midnights[i + 1]
            self.get_ohlcv_for_coin_for_day(cur_midnight, next_midnight, symbol, cat)

    # =============================================================================
    # Get ohlcv from BINANCE
    # =============================================================================
    def get_ohlcv_for_coin_for_day(
        self, cur_midnight: int, next_midnight: int, symbol: str, cat: str
    ):
        df = None
        limit = self.MINUTES_PER_DAY + 2  # give some extra room
        since = cur_midnight
        exceptions = 0
        while limit > 0:
            try:
                res = self.fetch_ohlcv_from_api(symbol, cat, since, limit)
                df = self.process_ohlcv_to_df(df, res)
                since = self.determine_since_for_pagination(df)
                limit -= len(df.index)
                self.sleep_for_exchange(cat)
            except Exception:
                traceback.print_exc()
                exceptions += 1
                print(f"Exceptions: {exceptions}")
            if self.MAX_EXCEPTIONS < exceptions:
                break

        df = self.process_final_df(next_midnight, df)
        self.save_df_to_s3(cur_midnight, symbol, cat, df)

    # =============================================================================
    # Fetch data, determine if futures or spot
    # =============================================================================
    def fetch_ohlcv_from_api(self, symbol: str, cat: str, since, limit):
        if cat == "spot":
            return BINANCE_SPOT.fetchOHLCV(
                symbol=symbol, timeframe=self.timeframe, since=since, limit=limit
            )
        elif cat == "futures":
            return BINANCE_FUTURES.fetchOHLCV(
                symbol=symbol, timeframe=self.timeframe, since=since, limit=limit
            )

    # =============================================================================
    # If df is None, create, else concat
    # =============================================================================
    def process_ohlcv_to_df(self, df, res):
        res = pd.DataFrame(res, columns=self.HEADER)
        if df is None:
            return res
        return pd.concat([df, res], ignore_index=True)

    # =============================================================================
    # Process datetime, drop duplicates, etc for final df
    # =============================================================================
    def process_final_df(self, next_midnight: int, df):
        df = df.drop_duplicates(subset="timestamp", keep="last")
        df = df[df["timestamp"] < next_midnight]
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df = df.set_index("timestamp")
        print(df)
        return df

    # =============================================================================
    # Save df to s3
    # =============================================================================
    def save_df_to_s3(self, unix: int, symbol: str, cat: str, df):
        if len(df.index) == 0:
            print("Nothing to save...")
            return
        date = dt.datetime.fromtimestamp(unix / 1000, tz=pytz.UTC).strftime("%Y-%m-%d")
        if cat == "futures":
            symbol = f"{symbol}-futures"

        path = f"{symbol}/{symbol}_{date}_ohlcv.csv"
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        res = S3.put_object(Bucket=BUCKET_NAME, Key=path, Body=csv_buffer.getvalue())
        print(
            f"Saved {symbol}. Status code: {res['ResponseMetadata']['HTTPStatusCode']}"
        )

    # =============================================================================
    #
    # HELPERS
    #
    # =============================================================================

    # =============================================================================
    # If no dates are provided use last full day
    # =============================================================================
    def determine_start_n_end_time(self, start_str=None, end_str=None):
        now = dt.datetime.utcnow().replace(tzinfo=pytz.UTC)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        self.start = self.determine_start_date(today, start_str)
        self.end = self.determine_end_date(today, end_str)

    # =============================================================================
    # Determine start, last full day if None provided
    # =============================================================================
    def determine_start_date(self, today, start_str=None):
        if start_str is None:
            yesterday = today - dt.timedelta(days=1)
            return int(dt.datetime.timestamp(yesterday)) * 1000
        return self.convert_date_str_to_utc_unix(start_str)

    # =============================================================================
    # Determine end, today if None provided
    # =============================================================================
    def determine_end_date(self, today, end_str=None):
        if end_str is None:
            return int(dt.datetime.timestamp(today)) * 1000
        return self.convert_date_str_to_utc_unix(end_str)

    # =============================================================================
    # Create list of all dates that we fetch for
    # =============================================================================
    def create_list_of_all_midnights(self):
        midnights = []
        cur = self.start
        MS_PER_DAY = 24 * 60 * 60 * 1000
        while cur <= self.end:
            midnights.append(cur)
            cur += MS_PER_DAY
        self.midnights = midnights

    # =============================================================================
    # Need to use pagination, hence, update since if already iterating
    # =============================================================================
    def determine_since_for_pagination(self, df):
        return df["timestamp"].iloc[-1]

    # =============================================================================
    # Need to use pagination, hence, update since if already iterating
    # =============================================================================
    def sleep_for_exchange(self, category):
        if category == "futures":
            time.sleep(BINANCE_FUTURES.rateLimit / 1000)
        else:
            time.sleep(BINANCE_SPOT.rateLimit / 1000)

    # =============================================================================
    # Convert date string like "2022-12-24" to UTC unix
    # =============================================================================
    def convert_date_str_to_utc_unix(self, date_str):
        date_obj = dt.datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
        return int(dt.datetime.timestamp(date_obj)) * 1000


if __name__ == "__main__":

    coins = [
        {"category": "spot", "symbol": "1INCHBUSD"},
        {"category": "spot", "symbol": "AAVEBUSD"},
        {"category": "spot", "symbol": "ADABUSD"},
        {"category": "spot", "symbol": "ALGOBUSD"},
        {"category": "spot", "symbol": "APEBUSD"},
        {"category": "spot", "symbol": "ATOMBUSD"},
        {"category": "spot", "symbol": "AVAXBUSD"},
        {"category": "spot", "symbol": "AXSBUSD"},
        {"category": "spot", "symbol": "BCHBUSD"},
        {"category": "spot", "symbol": "BNBBUSD"},
        {"category": "spot", "symbol": "BTCBUSD"},
        {"category": "spot", "symbol": "CAKEBUSD"},
        {"category": "spot", "symbol": "CHZBUSD"},
        {"category": "spot", "symbol": "COMPBUSD"},
        {"category": "spot", "symbol": "DASHBUSD"},
        {"category": "spot", "symbol": "DOGEBUSD"},
        {"category": "spot", "symbol": "DOTBUSD"},
        {"category": "spot", "symbol": "EGLDBUSD"},
        {"category": "spot", "symbol": "EOSBUSD"},
        {"category": "spot", "symbol": "ETCBUSD"},
        {"category": "spot", "symbol": "ETHBUSD"},
        {"category": "spot", "symbol": "FILBUSD"},
        {"category": "spot", "symbol": "FLOWBUSD"},
        {"category": "spot", "symbol": "FTMBUSD"},
        {"category": "spot", "symbol": "GRTBUSD"},
        {"category": "spot", "symbol": "HBARBUSD"},
        {"category": "spot", "symbol": "ICPBUSD"},
        {"category": "spot", "symbol": "IOTABUSD"},
        {"category": "spot", "symbol": "LDOBUSD"},
        {"category": "spot", "symbol": "LINKBUSD"},
        {"category": "spot", "symbol": "LTCBUSD"},
        {"category": "spot", "symbol": "LUNCBUSD"},
        {"category": "spot", "symbol": "MANABUSD"},
        {"category": "spot", "symbol": "MATICBUSD"},
        {"category": "spot", "symbol": "MKRBUSD"},
        {"category": "spot", "symbol": "NEARBUSD"},
        {"category": "spot", "symbol": "PAXGBUSD"},
        {"category": "spot", "symbol": "QNTBUSD"},
        {"category": "spot", "symbol": "SANDBUSD"},
        {"category": "spot", "symbol": "SHIBBUSD"},
        {"category": "spot", "symbol": "SOLBUSD"},
        {"category": "spot", "symbol": "SUSHIBUSD"},
        {"category": "spot", "symbol": "THETABUSD"},
        {"category": "spot", "symbol": "TRXBUSD"},
        {"category": "spot", "symbol": "TWTBUSD"},
        {"category": "spot", "symbol": "UNIBUSD"},
        {"category": "spot", "symbol": "VETBUSD"},
        {"category": "spot", "symbol": "WBTCBUSD"},
        {"category": "spot", "symbol": "XLMBUSD"},
        {"category": "spot", "symbol": "XMRBUSD"},
        {"category": "spot", "symbol": "XRPBUSD"},
        {"category": "spot", "symbol": "XTZBUSD"},
        {"category": "spot", "symbol": "ZECBUSD"},
        {"category": "futures", "symbol": "BTCBUSD"},
    ]
    if len(sys.argv) == 1:
        start_str = None
    elif len(sys.argv) == 2:
        start_str = sys.argv[1]

    obj = OhlcvPuller(coins, "1m", start_str=start_str)
    obj.main()
