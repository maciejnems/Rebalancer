import pandas as pd
import matplotlib.pyplot as plt
from rebalancer import utils
import numpy as np

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
    # "doge",
    "ada",
    "link",
    "Uni",
]

historical_data = utils.get_historical_data(
    tokens_popular_2021, "2020-10-01 00:00:00 UTC", "2022-08-25 00:00:00 UTC")


fig = plt.figure()
plt.grid()
for name, df in historical_data.items():
    x = pd.to_datetime(df['snapped_at'])
    plt.plot(x, df['total_volume'].rolling(7).mean(), label=name)

plt.ylim(0, None)
plt.legend(loc="upper left")


fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
x = pd.to_datetime(next(iter(historical_data.values()))['snapped_at'])
y = np.vstack([df['total_volume'].rolling(7).mean()
              for df in historical_data.values()])
labs = [name for name in historical_data.keys()]
ax = plt.gca()
ax.stackplot(x, y, labels=labs, alpha=0.8)
ax.legend(fontsize=10, ncol=4)
plt.show()
