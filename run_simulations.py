import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations import dex_exp
from simulations.simulate import exp, REBALANCE

exec_mode = ExecutionMode()

# Single Process Execution using a Single System Model Configuration:
local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
sys_model_simulation = Executor(
    exec_context=local_proc_ctx, configs=exp.configs)

sys_model_raw_result, sys_model_tensor_field, sessions = sys_model_simulation.execute()
sys_model_result = pd.DataFrame(sys_model_raw_result)
final_results = {row.run:  pd.DataFrame([row.profit]) for i, row in sys_model_result.iterrows()}
final_results = pd.concat(final_results.values(), axis=0)
final_results.to_csv("output.csv")
print("Rebalance: ", REBALANCE)
print(final_results)
# print(tabulate(final_results, headers='keys', tablefmt='psql'))
# print()
