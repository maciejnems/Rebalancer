from rebalancer.names import HEDGING, POPULARITY_CACHE, SWAP, UPDATE_INTERVAL
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
    "eos",
    "bch",
    "xrp",
    "link",
    "dot",
    "trx",
    "doge",
    "ada",
    "usdc",
]


# All
historical_data = utils.get_historical_data(
    tokens_popular_2021, "2020-09-01 00:00:00 UTC", "2022-09-01 00:00:00 UTC")

# During dogecoin
# historical_data = utils.get_historical_data(
#     tokens_popular_2021, "2020-09-01 00:00:00 UTC", "2021-07-01 00:00:00 UTC")

# After dogecoin
# historical_data = utils.get_historical_data(
#     tokens_popular_2021, "2021-07-01 00:00:00 UTC", "2022-09-01 00:00:00 UTC")

# Short
# historical_data = utils.get_historical_data(
#     tokens_popular_2021, "2022-08-20 00:00:00 UTC", "2022-08-25 00:00:00 UTC")

days = len(next(iter(historical_data.values()))) - 1
blocks = TX_PER_DAY * days

blocks, trading_volumes = utils.get_tx_per_day(historical_data, blocks)

print("Simulating...")
print("average tx per day:", TX_PER_DAY)
print("max tx per day:", max(trading_volumes))
print("min tx per day:", min(trading_volumes))
print("days:", days)
print("blocks:", blocks)

for i in range(1, 21):
    simulate_rebalancing_target_ratios.append(
        dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [7], HEDGING: [True], SWAP: [i*1000]}, historical_data, trading_volumes)
    simulate_equal_target_ratios.append(
        dex_exp, blocks, {UPDATE_INTERVAL: [None], POPULARITY_CACHE: [None], HEDGING: [True], SWAP: [i*1000]}, historical_data, trading_volumes)

for i in range(1, 22):
    simulate_rebalancing_target_ratios.append(
        dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [i], HEDGING: [True], SWAP: [7000]}, historical_data, trading_volumes)
for i in range(1, 61):
    simulate_rebalancing_target_ratios.append(
        dex_exp, blocks, {UPDATE_INTERVAL: [i], POPULARITY_CACHE: [7], HEDGING: [True], SWAP: [7000]}, historical_data, trading_volumes)
