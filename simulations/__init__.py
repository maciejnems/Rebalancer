from cadCAD.configuration import Experiment
from simulations import simulate_equal_target_ratios, simulate_rebalancing_target_ratios
from rebalancer.model import TX_PER_DAY
from rebalancer import utils

dex_exp = Experiment()
# BLOCKS = 96000

tokens_popular_2021 = [
    # "usdt",
    # "btc",
    # "eth",
    "ltc",
    "bch",
    "xrp",
    "eos",
    "dot",
    "busd",
    "doge",
    "ada",
    "link",
    "Uni",
]

# historical_data = utils.get_historical_data(
#     tokens_popular_2021, "2020-10-01 00:00:00 UTC", "2022-08-25 00:00:00 UTC")
historical_data = utils.get_historical_data(tokens_popular_2021, "2021-07-01 00:00:00 UTC", "2022-08-25 00:00:00 UTC")

days = len(next(iter(historical_data.values()))) - 1
blocks = TX_PER_DAY * days

print("Simulating, days:", days, "blocks:", blocks)
simulate_rebalancing_target_ratios.append(dex_exp, blocks, 7, historical_data)
simulate_rebalancing_target_ratios.append(dex_exp, blocks, 14, historical_data)
simulate_rebalancing_target_ratios.append(dex_exp, blocks, 21, historical_data)
simulate_equal_target_ratios.append(dex_exp, blocks, historical_data)
