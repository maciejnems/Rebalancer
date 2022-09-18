import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
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


exec_mode = ExecutionMode()

# Single Process Execution using a Single System Model Configuration:
local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
sys_model_simulation = Executor(
    exec_context=local_proc_ctx, configs=dex_exp.configs)

sys_model_raw_result, sys_model_tensor_field, sessions = sys_model_simulation.execute()
sys_model_result = pd.DataFrame(sys_model_raw_result)
confs = [(conf.model_id, len(conf.sim_config["T"]))
         for conf in dex_exp.configs]
confs = [(conf.model_id, conf.sim_config["M"], days)
         for conf in dex_exp.configs]
final_results = {}

counter = -1
for (id, m, len) in confs:
    counter += len + 1
    final_results[id] = pd.DataFrame([id])
    final_results[id]["interval"] = m[names.UPDATE_INTERVAL]
    final_results[id]["cache"] = m[names.POPULARITY_CACHE]
    final_results[id]["hedging"] = m[names.HEDGING]
    final_results[id]["arbitrageur"] = sys_model_result.iloc[counter].profit[names.ARBITRAGEUR_PROFIT][0]
    final_results[id]["normal"] = sys_model_result.iloc[counter].profit[names.NORMAL_PROFIT][0]
    final_results[id]["avg loss"] = (sys_model_result.iloc[counter].profit[names.NORMAL_PROFIT][1] +
                                     sys_model_result.iloc[counter].profit[names.NORMAL_PROFIT][2]) / sys_model_result.iloc[counter].profit[names.NORMAL_PROFIT][0]
    final_results[id]["days"] = sys_model_result.iloc[counter].timestamp.day
    final_results[id]["v"] = formulas.compute_V(
        sys_model_result.iloc[counter][names.POOL])
    # for t in sys_model_result.iloc[counter][names.POOL].values():
    #     final_results[id][t.name] = t.target_ratio


x = pd.to_datetime(next(iter(historical_data.values()))["snapped_at"])

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
    plt.plot(x, df[0], label=id)
plt.legend(fontsize=12, ncol=5)
plt.gcf().autofmt_xdate()
plt.ylim(0, None)
plt.xlim(pd.to_datetime("2020-09-08 00:00:00 UTC"),
         pd.to_datetime("2022-09-01 00:00:00 UTC"))
plt.title("Value of liquidity pools", fontsize=16)
plt.ylabel("Pool Value (USD)")
ax.yaxis.set_major_formatter(formatter)
fig.tight_layout()


counter = 0
for (id, m, len) in confs:
    df = []
    for i in range(counter, counter+len+1):
        df.append(
            sys_model_result.iloc[i][names.POOL])
    counter += len + 1
    df = pd.DataFrame(df)
    df = df.applymap(lambda t: t.balance * t.price).transpose()
    fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=90)
    ax.yaxis.set_major_formatter(formatter)
    labs = [name for name in historical_data.keys()]
    ax = plt.gca()
    ax.stackplot(x, df, labels=labs, alpha=0.8)
    plt.title(id, fontsize=16)
    plt.gcf().autofmt_xdate()
    plt.ylim(0, None)
    plt.xlim(pd.to_datetime("2020-09-08 00:00:00 UTC"),
             pd.to_datetime("2022-09-01 00:00:00 UTC"))
    ax.legend(fontsize=12, ncol=5)
    plt.ylabel("Pool Value (USD)")


final_results = pd.concat(final_results.values(), axis=0)
final_results.to_csv("output.csv")
print(tabulate(final_results, headers='keys', tablefmt='psql'))
# print(tabulate(sys_model_result, headers='keys', tablefmt='psql'))

plt.show()
