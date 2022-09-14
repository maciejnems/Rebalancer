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

# Start
# historical_data = utils.get_historical_data(
#     tokens_popular_2021, "2020-10-01 00:00:00 UTC", "2022-08-25 00:00:00 UTC")

# During dogecoin
historical_data = utils.get_historical_data(
    tokens_popular_2021, "2020-10-01 00:00:00 UTC", "2021-07-01 00:00:00 UTC")

# After dogecoin
# historical_data = utils.get_historical_data(
#     tokens_popular_2021, "2021-07-01 00:00:00 UTC", "2022-08-25 00:00:00 UTC")

# Short
# historical_data = utils.get_historical_data(tokens_popular_2021, "2022-08-01 00:00:00 UTC", "2022-08-25 00:00:00 UTC")

days = len(next(iter(historical_data.values()))) - 1
blocks = TX_PER_DAY * days

blocks, trading_volumes = utils.get_tx_per_day(historical_data, blocks)

print("Simulating...")
print("average tx per day:", TX_PER_DAY)
print("max tx per day:", max(trading_volumes))
print("min tx per day:", min(trading_volumes))
print("days:", days)
print("blocks:", blocks)
simulate_rebalancing_target_ratios.append(
    dex_exp, blocks, 1, historical_data, trading_volumes)
simulate_rebalancing_target_ratios.append(
    dex_exp, blocks, 7, historical_data, trading_volumes)
simulate_rebalancing_target_ratios.append(
    dex_exp, blocks, 14, historical_data, trading_volumes)
simulate_equal_target_ratios.append(
    dex_exp, blocks, historical_data, trading_volumes)
