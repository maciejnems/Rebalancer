import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations import dex_exp
from rebalancer import formulas

exec_mode = ExecutionMode()

print(dex_exp.configs)
# Single Process Execution using a Single System Model Configuration:
local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
sys_model_simulation = Executor(
    exec_context=local_proc_ctx, configs=dex_exp.configs)

sys_model_raw_result, sys_model_tensor_field, sessions = sys_model_simulation.execute()
sys_model_result = pd.DataFrame(sys_model_raw_result)
confs = [(conf.model_id, len(conf.sim_config["T"]))
         for conf in dex_exp.configs]
confs = [(conf.model_id, 6000) for conf in dex_exp.configs]
counter = -1
final_results = {}

for (id, len) in confs:
    counter += len + 1
    final_results[id] = pd.DataFrame([sys_model_result.iloc[counter].profit])
    final_results[id]["simulation"] = id
    final_results[id]["average loss"] = (sys_model_result.iloc[counter].profit["profit-normal"][1] +
                                         sys_model_result.iloc[counter].profit["profit-normal"][2]) / sys_model_result.iloc[counter].profit["profit-normal"][0]
    final_results[id]["n"] = sys_model_result.iloc[counter].block
    final_results[id]["v"] = formulas.compute_V(
        sys_model_result.iloc[counter]["pool"])

final_results = pd.concat(final_results.values(), axis=0)
final_results.to_csv("output.csv")
print(tabulate(final_results, headers='keys', tablefmt='psql'))
