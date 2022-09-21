import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_computed_result():
    data = pd.read_csv("computed_result.csv")
    rebalancer = data[data['0'] == "Rebalancer"].reset_index()
    balancer = data[data['0'] == "Balancer"].reset_index()

    fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=90)
    plt.grid()
    for name, df in [("Rebalancer", rebalancer), ("Balancer", balancer)]:
        x = df['swap-mean']
        y = -df['avg loss']
        plt.plot(x, y, label=name)

    plt.title("Price impact average loss", fontsize=16)
    plt.gcf().autofmt_xdate()
    plt.ylim(0, None)
    plt.xlim(0, None)
    plt.legend(fontsize=12, ncol=5)

    plt.ylabel("average loss (USD)")
    plt.xlabel("swap value (USD)")
    fig.tight_layout()


def plot_cache_result():
    data = pd.read_csv("cache_result.csv")
    rebalancer = data[data['0'] == "Rebalancer"].reset_index()
    balancer = data[data['0'] == "Balancer"].reset_index()

    x = rebalancer['cache']
    y = -rebalancer['avg loss']

    model2 = np.poly1d(np.polyfit(x, y, 2))
    X_ = np.linspace(x.min(), x.max(), 500)
    Y_ = model2(X_)

    fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=90)
    plt.grid()
    plt.plot(x, y, "bo", label="Rebalancer results", linestyle='--', alpha=0.7)
    plt.plot(X_, Y_, label="Rebalancer approximation", c='r')
    plt.axhline(y=-balancer.iloc[0]["avg loss"],
                label='Balancer',  color="orange")
    plt.ylim(0.95 * min(-rebalancer['avg loss']
                        ), -balancer.iloc[0]["avg loss"] * 1.05)
    ax.set_yticks([y.min(), y.max(), -balancer.iloc[0]["avg loss"]])
    plt.legend(fontsize=12)
    plt.xlim(min(rebalancer['cache']), max(rebalancer['cache']))
    plt.ylabel("price impact average loss (USD)")
    plt.xlabel("trading volume cache size in days")
    fig.tight_layout()


def plot_interval_result():
    data = pd.read_csv("interval_result.csv")
    rebalancer = data[data['0'] == "Rebalancer"].reset_index()
    balancer = data[data['0'] == "Balancer"].reset_index()

    x = rebalancer['interval']
    y = -rebalancer['avg loss']

    model2 = np.poly1d(np.polyfit(x, y, 2))
    X_ = np.linspace(x.min(), x.max(), 500)
    Y_ = model2(X_)
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=90)
    plt.grid()
    plt.plot(x, y, "bo", label="Rebalancer results", linestyle='--', alpha=0.7)
    plt.plot(X_, Y_, label="Rebalancer approximation", c='r')
    plt.axhline(y=-balancer.iloc[0]["avg loss"],
                label='Balancer',  color="orange")
    plt.ylim(0.95 * min(-rebalancer['avg loss']
                        ), -balancer.iloc[0]["avg loss"] * 1.05)
    plt.legend(fontsize=12)
    plt.xlim(min(rebalancer['interval']), max(rebalancer['interval']))
    plt.ylabel("price impact average loss (USD)")
    plt.xlabel("update interval length in days")
    ax.set_yticks([y.min(), y.max(), max(Y_), min(
        Y_), -balancer.iloc[0]["avg loss"]])
    fig.tight_layout()


plot_computed_result()
plot_cache_result()
plot_interval_result()
plt.show()
