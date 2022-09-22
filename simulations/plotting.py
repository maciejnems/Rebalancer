import pandas as pd
from simulations import dex_exp, days, historical_data
from rebalancer import formulas, names
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt


def human_format(num, pos):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '$%.2f %s' % (num, ['', 'K', 'M', 'B', 'T'][magnitude])


formatter = FuncFormatter(human_format)


def plt_pool_values(sys_model_result, confs, timestamps):
    fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=90)
    plt.grid()
    counter = 0
    for (id, m, len) in confs:
        df = []
        for i in range(counter, counter+len+1):
            df.append([formulas.compute_V(
                sys_model_result.iloc[i][names.POOL])])
        counter += len + 1
        df = pd.DataFrame(df)
        plt.plot(timestamps, df[0], label=id)
    plt.legend(fontsize=12, ncol=5)
    plt.gcf().autofmt_xdate()
    plt.ylim(0, None)
    plt.xlim(pd.to_datetime("2020-09-08 00:00:00 UTC"),
             pd.to_datetime("2022-09-01 00:00:00 UTC"))
    plt.title("Value of liquidity pools", fontsize=16)
    plt.ylabel("Pool Value (USD)")
    ax.yaxis.set_major_formatter(formatter)
    fig.tight_layout()


def plt_pool_distributions(sys_model_result, confs, timestamps):
    counter = 0
    for (id, m, len) in confs:
        df = []
        for i in range(counter, counter+len+1):
            df.append(
                sys_model_result.iloc[i][names.POOL])
        labs = [name for name in sys_model_result.iloc[counter][names.POOL].keys()]
        counter += len + 1
        df = pd.DataFrame(df)
        df = df.applymap(lambda t: t.balance * t.price).transpose()
        fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=90)
        ax.yaxis.set_major_formatter(formatter)
        ax = plt.gca()
        ax.stackplot(timestamps, df, labels=labs, alpha=0.8)
        plt.title(id, fontsize=16)
        plt.gcf().autofmt_xdate()
        plt.ylim(0, None)
        plt.xlim(pd.to_datetime("2020-09-08 00:00:00 UTC"),
                 pd.to_datetime("2022-09-01 00:00:00 UTC"))
        ax.legend(fontsize=12, ncol=5)
        plt.ylabel("Pool Value (USD)")


def plt_daily_loss(sys_model_result, confs, timestamps):
    fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=90)
    plt.grid()
    counter = 0
    for (id, m, len) in confs:
        tx_count = []
        loss = []
        for i in range(counter, counter+len+1):
            tx_count.append(
                sys_model_result.iloc[i].users[names.NORMAL].tx_count)
            loss.append(
                sys_model_result.iloc[i].users[names.NORMAL].loss + sys_model_result.iloc[i].users[names.NORMAL].profit)
        # df =                 sys_model_result.iloc[counter: counter+len+1].users
        counter += len + 1
        tx_count = pd.DataFrame(tx_count)
        loss = pd.DataFrame(loss)
        tx_count = tx_count.iloc[1:].reset_index(drop=True) - tx_count.iloc[:-1]
        loss = loss.iloc[1:].reset_index(drop=True) - loss.iloc[:-1]
        y = (-loss / tx_count)[0]
        plt.plot(timestamps.iloc[1:], y.rolling(7).mean(), label=id)
        plt.legend(fontsize=12, ncol=5)
        plt.gcf().autofmt_xdate()
        # plt.ylim(0, None)
        plt.xlim(pd.to_datetime("2020-09-08 00:00:00 UTC"),
                 pd.to_datetime("2022-09-01 00:00:00 UTC"))
        plt.title("Loss per day", fontsize=16)
        plt.ylabel("Loss (USD)")
        ax.yaxis.set_major_formatter(formatter)
        fig.tight_layout()

# def plt_daily_loss_mean(sys_model_result, confs, timestamps):
#     fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=90)
#     plt.grid()
#     counter = 0
#     for (id, m, len) in confs:
#         tx_count = []
#         loss = []
#         for i in range(counter, counter+len+1):
#             tx_count.append(
#                 sys_model_result.iloc[i].users[names.NORMAL].tx_count)
#             loss.append(
#                 sys_model_result.iloc[i].users[names.NORMAL].loss + sys_model_result.iloc[i].users[names.NORMAL].profit)
#         # df =                 sys_model_result.iloc[counter: counter+len+1].users
#         counter += len + 1
#         tx_count = pd.DataFrame(tx_count)
#         loss = pd.DataFrame(loss)
#         tx_count = tx_count.iloc[1:].reset_index(drop=True) - tx_count.iloc[:-1]
#         loss = loss.iloc[1:].reset_index(drop=True) - loss.iloc[:-1]
#         y = (-loss / tx_count)[0]
#         plt.plot(timestamps.iloc[1:], y.rolling(14).mean(), label=id)
#         plt.legend(fontsize=12, ncol=5)
#         plt.gcf().autofmt_xdate()
#         # plt.ylim(0, None)
#         plt.xlim(pd.to_datetime("2020-09-08 00:00:00 UTC"),
#                  pd.to_datetime("2022-09-01 00:00:00 UTC"))
#         plt.title("Loss per day", fontsize=16)
#         plt.ylabel("Loss (USD)")
#         ax.yaxis.set_major_formatter(formatter)
#         fig.tight_layout()

