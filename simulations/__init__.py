from cadCAD.configuration import Experiment
from simulations import simulate_equal_target_ratios, simulate_rebalancing_target_ratios

dex_exp = Experiment()
BLOCKS = 96000


simulate_rebalancing_target_ratios.append(dex_exp, BLOCKS, 7)
simulate_rebalancing_target_ratios.append(dex_exp, BLOCKS, 14)
simulate_rebalancing_target_ratios.append(dex_exp, BLOCKS, 21)
simulate_equal_target_ratios.append(dex_exp, BLOCKS)
