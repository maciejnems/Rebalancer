from cadCAD.configuration import Experiment
from simulations import simulate_equal_target_ratios, simulate_rebalancing_target_ratios

dex_exp = Experiment()
BLOCKS = 60000


simulate_rebalancing_target_ratios.append(dex_exp, BLOCKS)
simulate_equal_target_ratios.append(dex_exp, BLOCKS)
