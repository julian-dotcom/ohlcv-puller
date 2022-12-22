# =============================================================================
# IMPORTS
# =============================================================================
import os
import boto3
from dotenv import load_dotenv
import pandas as pd
from pprint import pprint

pd.options.plotting.backend = "plotly"
load_dotenv()
# =============================================================================
# CONFIG
# =============================================================================
BUCKET_NAME = "binance-ohlcv"
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name="eu-central-1",
)
folders = S3.list_objects_v2(Bucket=BUCKET_NAME, Delimiter="/")["CommonPrefixes"]
folders = [f["Prefix"] for f in folders]
### ============================================================
### ENTER TOKEN NAME YOU WANT TO VISUALIZE HERE
TOKEN = "BTC"
###
### ============================================================
folder = f"{TOKEN}BUSD-futures/"
files = S3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=folder)
files = [f["Key"] for f in files["Contents"]]
df = None
for file in files:
    print(file)
    csv = S3.get_object(Bucket=BUCKET_NAME, Key=file)
    if df is None:
        df = pd.read_csv(csv["Body"])
        continue
    temp = pd.read_csv(csv["Body"])
    df = pd.concat([df, temp], ignore_index=True)

df = df.set_index("timestamp")
fig = df["close"].plot(
    title=f"{TOKEN} OHLCV",
    template="simple_white",
    labels=dict(index="date", value="Close"),
)
fig.update_yaxes(tickprefix="$")
fig.show()
