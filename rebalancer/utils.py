import pandas as pd

tokens = [
    # "usdt",
    "usdc",
    # "eth",
    # "btc",
    "bnb",
    "dot",
    "sol",
    "xrp",
]


def read_csv(token_file):
    data = pd.read_csv(token_file)
    data = data[data.snapped_at >= "2021-01-01 00:00:00 UTC"]
    data = data[data.snapped_at <= "2022-08-25 00:00:00 UTC"]
    return data


def get_historical_data():
    token_files = [f"data/{t}-usd-max.csv" for t in tokens]
    return {t: read_csv(f) for t, f in zip(tokens, token_files)}
