# =============================================================================
# IMPORTS
# =============================================================================
import os, pytz, time, traceback
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
BINANCE = ccxt.binance()
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

    def __init__(self, coins, timeframe, start_str, end_str=None):
        self.coins = coins
        self.timeframe = timeframe
        self.determine_start_n_end_time(start_str, end_str)
        self.create_list_of_all_midnights()

    # =============================================================================
    # MAIN
    # =============================================================================
    def main(self):
        for coin in self.coins:
            self.get_ohlcv_for_coin_for_all_dates(coin)

    # =============================================================================
    # Iterate over all dates, fetch for every single date
    # =============================================================================
    def get_ohlcv_for_coin_for_all_dates(self, coin):
        for i in range(len(self.midnights) - 1):
            print(coin)
            cur_midnight, next_midnight = self.midnights[i], self.midnights[i + 1]
            self.get_ohlcv_for_coin_for_date(cur_midnight, next_midnight, coin)

    # =============================================================================
    # Get ohlcv from BINANCE
    # =============================================================================
    def get_ohlcv_for_coin_for_date(self, cur_midnight: int, next_midnight: int, coin):
        df = None
        limit = self.MINUTES_PER_DAY + 2  # give some extra room
        since = cur_midnight
        while limit > 0:
            try:
                res = BINANCE.fetchOHLCV(
                    symbol=coin, timeframe=self.timeframe, since=since, limit=limit
                )
                df = self.process_ohlcv_to_df(df, res)
                since = self.determine_since_for_pagination(df)
                limit -= len(df.index)
                self.sleep_for_exchange()
            except Exception:
                traceback.print_exc()

        df = self.process_final_df(next_midnight, df)
        self.save_df_to_s3(cur_midnight, coin, df)

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
    def save_df_to_s3(self, unix: int, coin: str, df):
        if len(df.index) == 0:
            print("Nothing to save...")
            return
        date = dt.datetime.fromtimestamp(unix / 1000, tz=pytz.UTC).strftime("%Y-%m-%d")
        path = f"{coin}/{coin}_{date}_ohlcv.csv"
        csv_buffer = StringIO()
        df.to_csv(csv_buffer)
        res = S3.put_object(Bucket=BUCKET_NAME, Key=path, Body=csv_buffer.getvalue())
        print(f"Saved {coin}. Status code: {res['ResponseMetadata']['HTTPStatusCode']}")

    # =============================================================================
    #
    # HELPERS
    #
    # =============================================================================

    # =============================================================================
    # If no dates are provided use last full day
    # =============================================================================
    def determine_start_n_end_time(self, start_str, end_str=None):
        now = dt.datetime.utcnow().replace(tzinfo=pytz.UTC)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        self.start = self.convert_date_str_to_utc_unix(start_str)
        if end_str is None:
            self.end = int(dt.datetime.timestamp(today)) * 1000
        else:
            self.end = self.convert_date_str_to_utc_unix(end_str)

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
    def sleep_for_exchange(self):
        time.sleep(BINANCE.rateLimit / 1000)

    # =============================================================================
    # Convert date string like "2022-12-24" to UTC unix
    # =============================================================================
    def convert_date_str_to_utc_unix(self, date_str):
        date_obj = dt.datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
        return int(dt.datetime.timestamp(date_obj)) * 1000


if __name__ == "__main__":
    coins = [
        # "ADABUSD",
        # "ALGOBUSD",
        "APEBUSD",
        "ATOMBUSD",
        "AVAXBUSD",
        "BNBBUSD",
        "BTCBUSD",
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
        "TRXBUSD",
        "UNIBUSD",
        "VETBUSD",
        "XLMBUSD",
        "XMRBUSD",
        "XRPBUSD",
    ]

    obj = OhlcvPuller(coins, "1m", start_str="2021-06-01")
    obj.main()
