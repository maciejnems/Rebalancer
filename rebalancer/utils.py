import pandas as pd

tokens_popular_now = [
    # "usdt",
    "usdc",
    # "eth",
    # "btc",
    "ada",
    "bnb",
    # "dai",
    "dot",
    "matic",
    "sol",
    "xrp",
]


def read_csv(token_file, start, end):
    data = pd.read_csv(token_file)
    data = data[data.snapped_at >= start]
    data = data[data.snapped_at <= end]
    data.reset_index(drop=True, inplace=True)
    return data


def get_historical_data(token_names, start, end):
    token_files = [f"data/{t}-usd-max.csv" for t in token_names]
    return {t: read_csv(f, start, end) for t, f in zip(token_names, token_files)}
