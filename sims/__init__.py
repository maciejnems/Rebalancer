from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import config_sim
from sims import simulate_rebalancing_target_ratios, simulate_equal_target_ratios

sim_config = config_sim(
    {
        "N": 1,
        "T": range(20000),
    }
)

dex_exp = Experiment()

simulate_rebalancing_target_ratios.append(dex_exp, sim_config)
simulate_equal_target_ratios.append(dex_exp, sim_config)
