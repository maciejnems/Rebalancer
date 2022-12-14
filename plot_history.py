import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from rebalancer import utils
import numpy as np

# Tokens used for set of 10 tokens in paper
tokens_popular_2021 = [
    # "usdt",
    # "btc",
    # "eth",
    "ltc",
    "eos",
    "bch",
    "xrp",
    "link",
    "dot",
    "trx",
    "doge",
    "ada",
    "usdc",
]

# Tokens used for set of 5 tokens in paper
big_tokens = [
    "usdt",
    "eth",
    "xrp",
    "link",
    "bch",
]


def human_format(num, pos):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '$%.2f %s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])


formatter = FuncFormatter(human_format)


def plt_prices(historical_data):
    fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=90)
    plt.grid()
    for name, df in historical_data.items():
        x = pd.to_datetime(df['snapped_at'])
        plt.plot(x, df['price'].rolling(7).mean(), label=name)

    plt.title("Token prices 09-2020 to 09-2022", fontsize=16)
    plt.gcf().autofmt_xdate()
    plt.yscale("log")
    plt.xlim(pd.to_datetime("2020-09-08 00:00:00 UTC"),
             pd.to_datetime("2022-09-01 00:00:00 UTC"))
    plt.legend(fontsize=12, ncol=5)

    plt.ylabel("Price (USD)")
    ax.yaxis.set_major_formatter(formatter)
    fig.tight_layout()


def plt_trading_volume(historical_data):
    fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=90)
    plt.grid()
    for name, df in historical_data.items():
        x = pd.to_datetime(df['snapped_at'])
        plt.plot(x, df['total_volume'].rolling(7).mean(), label=name)

    plt.title("Trading volume 09-2020 to 09-2022", fontsize=16)
    plt.gcf().autofmt_xdate()
    plt.ylim(0, None)
    plt.xlim(pd.to_datetime("2020-09-08 00:00:00 UTC"),
             pd.to_datetime("2022-09-01 00:00:00 UTC"))
    plt.legend(fontsize=12, ncol=5)

    plt.ylabel("Trading Volume (USD)")
    ax.yaxis.set_major_formatter(formatter)
    plt.legend(loc="upper left")
    fig.tight_layout()


def plt_trading_volume_joined(historical_data):
    fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=90)
    x = pd.to_datetime(next(iter(historical_data.values()))['snapped_at'])
    y = np.vstack([df['total_volume'].rolling(7).mean()
                  for df in historical_data.values()])
    labs = [name for name in historical_data.keys()]
    ax = plt.gca()
    ax.stackplot(x, y, labels=labs, alpha=0.8)
    plt.title("Joined trading volume 09-2020 to 09-2022", fontsize=16)
    plt.gcf().autofmt_xdate()
    plt.ylim(0, None)
    plt.xlim(pd.to_datetime("2020-09-08 00:00:00 UTC"),
             pd.to_datetime("2022-09-01 00:00:00 UTC"))
    ax.legend(fontsize=12, ncol=5)
    ax.yaxis.set_major_formatter(formatter)
    plt.ylabel("Trading Volume (USD)")
    fig.tight_layout()


# For set of 10 tokens
historical_data_10 = utils.get_historical_data(
    tokens_popular_2021, "2020-09-01 00:00:00 UTC", "2022-09-01 00:00:00 UTC")

# For set of 5 tokens
historical_data_5 = utils.get_historical_data(
    big_tokens, "2020-09-01 00:00:00 UTC", "2022-09-01 00:00:00 UTC")

data = [historical_data_10, historical_data_5]

for hd in data:
    plt_prices(hd)
    plt_trading_volume(hd)
    plt_trading_volume_joined(hd)
plt.show()
