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

tokens_popular_2021 = [
    # "usdt",
    # "btc",
    # "eth",
    "ltc",
    "bch",
    "xrp",
    "eos",
    "dot",
    "busd",
    "doge",
    "ada",
    "link",
    "Uni",
]


def read_csv(token_file):
    data = pd.read_csv(token_file)
    data = data[data.snapped_at >= "2021-01-01 00:00:00 UTC"]
    # data = data[data.snapped_at >= "2021-03-01 00:00:00 UTC"]
    # data = data[data.snapped_at >= "2022-01-25 00:00:00 UTC"]
    # data = data[data.snapped_at >= "2022-08-01 00:00:00 UTC"]
    # data = data[data.snapped_at <= "2022-08-01 00:00:00 UTC"]
    data = data[data.snapped_at <= "2021-03-01 00:00:00 UTC"]
    # data.reset_index()
    data.reset_index(drop=True, inplace=True)
    return data


def get_historical_data():
    token_files = [f"data/{t}-usd-max.csv" for t in tokens_popular_2021]
    return {t: read_csv(f) for t, f in zip(tokens_popular_2021, token_files)}
