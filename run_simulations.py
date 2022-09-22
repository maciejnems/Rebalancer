import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations import dex_exp, days, historical_data, plotting
from rebalancer import formulas, names
import matplotlib.pyplot as plt


exec_mode = ExecutionMode()

# Single Process Execution using a Single System Model Configuration:
local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
sys_model_simulation = Executor(
    exec_context=local_proc_ctx, configs=dex_exp.configs)

sys_model_raw_result, sys_model_tensor_field, sessions = sys_model_simulation.execute()
sys_model_result = pd.DataFrame(sys_model_raw_result)

confs = [(conf.model_id, conf.sim_config["M"], days)
         for conf in dex_exp.configs]
final_results = {}

# Count result of simulation
counter = -1
for (id, m, len) in confs:
    counter += len + 1
    final_results[id] = pd.DataFrame([id])
    final_results[id]["interval"] = m[names.UPDATE_INTERVAL]
    final_results[id]["cache"] = m[names.POPULARITY_CACHE]
    final_results[id]["hedging"] = m[names.HEDGING]
    final_results[id]["swap-mean"] = m[names.SWAP]
    final_results[id]["arbitrageur"] = sys_model_result.iloc[counter].users[names.ARBITRAGEUR].tx_count
    final_results[id]["normal"] = sys_model_result.iloc[counter].users[names.NORMAL].tx_count
    final_results[id]["avg loss"] = (sys_model_result.iloc[counter].users[names.NORMAL].profit +
                                     sys_model_result.iloc[counter].users[names.NORMAL].loss) / sys_model_result.iloc[counter].users[names.NORMAL].tx_count
    final_results[id]["days"] = sys_model_result.iloc[counter].timestamp.day
    final_results[id]["v"] = formulas.compute_V(
        sys_model_result.iloc[counter][names.POOL])
    final_results[id]["tokens"] = [list(sys_model_result.iloc[counter][names.POOL].keys())]
    # for t in sys_model_result.iloc[counter][names.POOL].values():
    #     final_results[id][t.name] = t.target_ratio

# Print result of simulation
final_results = pd.concat(final_results.values(), axis=0)
final_results.to_csv("output.csv")
print(tabulate(final_results, headers='keys', tablefmt='psql'))
# print(tabulate(sys_model_result, headers='keys', tablefmt='psql'))

# Plot simulation
x = pd.to_datetime(next(iter(historical_data.values()))["snapped_at"])

# plotting.plt_daily_loss(sys_model_result, confs, x)
# plotting.plt_pool_values(sys_model_result, confs, x)
# plotting.plt_pool_distributions(sys_model_result, confs, x)

plt.show()
