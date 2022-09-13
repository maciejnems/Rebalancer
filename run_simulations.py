import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations import dex_exp
from rebalancer import formulas, names

exec_mode = ExecutionMode()

# Single Process Execution using a Single System Model Configuration:
local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
sys_model_simulation = Executor(
    exec_context=local_proc_ctx, configs=dex_exp.configs)

sys_model_raw_result, sys_model_tensor_field, sessions = sys_model_simulation.execute()
sys_model_result = pd.DataFrame(sys_model_raw_result)
confs = [(conf.model_id, len(conf.sim_config["T"]))
         for conf in dex_exp.configs]
confs = [(conf.model_id, conf.sim_config["M"], 10) for conf in dex_exp.configs]
counter = -1
final_results = {}

for (id, m, len) in confs:
    counter += len + 1
    final_results[id] = pd.DataFrame([id])
    final_results[id]["update interval"] = m[names.UPDATE_INTERVAL]
    final_results[id]["history cache"] = m[names.POPULARIT_CACHE]
    final_results[id]["average loss"] = (sys_model_result.iloc[counter].profit[names.NORMAL_PROFIT][1] +
                                         sys_model_result.iloc[counter].profit[names.NORMAL_PROFIT][2]) / sys_model_result.iloc[counter].profit[names.NORMAL_PROFIT][0]
    final_results[id]["n"] = sys_model_result.iloc[counter].block
    final_results[id]["v"] = formulas.compute_V(
        sys_model_result.iloc[counter][names.POOL])
    for t in sys_model_result.iloc[counter][names.POOL].values():
        final_results[id][t.name] = t.target_ratio

final_results = pd.concat(final_results.values(), axis=0)
final_results.to_csv("output.csv")
print(tabulate(final_results, headers='keys', tablefmt='psql'))
