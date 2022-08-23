import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulate import exp

exec_mode = ExecutionMode()

# Single Process Execution using a Single System Model Configuration:
local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
sys_model_simulation = Executor(
    exec_context=local_proc_ctx, configs=exp.configs)

sys_model_raw_result, sys_model_tensor_field, sessions = sys_model_simulation.execute()
sys_model_result = pd.DataFrame(sys_model_raw_result)
print()
print("Tensor Field: sys_model")
print(tabulate(sys_model_tensor_field, headers='keys', tablefmt='psql'))
print("Result: System Events DataFrame")
print(tabulate(sys_model_result, headers='keys', tablefmt='psql'))
print()
