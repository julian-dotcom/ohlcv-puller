# =============================================================================
# IMPORTS
# =============================================================================
import os, pytz, time
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

    def __init__(self, coins, timeframe, start=None):
        self.coins = coins
        self.timeframe = timeframe
        self.determine_start_time(start)

    # =============================================================================
    # MAIN
    # =============================================================================
    def main(self):
        for coin in self.coins:
            df = self.get_ohlcv_for_coins(coin)
            self.save_df_to_s3(coin, df)

    # =============================================================================
    # Get ohlcv
    # =============================================================================
    def get_ohlcv_for_coins(self, coin):
        df = None
        since = self.determine_since_for_pagination(df)
        while since < self.end:
            res = BINANCE.fetchOHLCV(
                symbol=coin,
                timeframe=self.timeframe,
                since=since,
            )
            df = self.process_ohlcv_to_df(df, res)
            since = self.determine_since_for_pagination(df)
            self.sleep_for_exchange()
        df = self.process_final_df(df)
        return df

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
    def process_final_df(self, df):
        df = df.drop_duplicates(subset="timestamp", keep="last")
        df = df[df["timestamp"] < self.end]
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df = df.set_index("timestamp")
        return df

    # =============================================================================
    # Save df to s3
    # =============================================================================
    def save_df_to_s3(self, coin, df):
        date = str(self.start_obj.date())
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
    def determine_start_time(self, start):
        now = dt.datetime.utcnow().replace(tzinfo=pytz.UTC)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        if start is None:
            start = today - dt.timedelta(days=1)
        else:
            start = dt.datetime.strptime(start, "%Y-%m-%d").replace(tzinfo=pytz.UTC)
        self.start_obj = start
        self.start = int(dt.datetime.timestamp(start)) * 1000
        self.end = int(dt.datetime.timestamp(today)) * 1000

    # =============================================================================
    # Need to use pagination, hence, update since if already iterating
    # =============================================================================
    def determine_since_for_pagination(self, df):
        if df is None:
            return self.start
        return df["timestamp"].iloc[-1]

    # =============================================================================
    # Need to use pagination, hence, update since if already iterating
    # =============================================================================
    def sleep_for_exchange(self):
        time.sleep(BINANCE.rateLimit / 1000)


if __name__ == "__main__":
    coins = ["ETHUSDT"]
    obj = OhlcvPuller(coins, "1m", start="2022-12-04")
    obj.main()
