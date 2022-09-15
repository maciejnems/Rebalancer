from rebalancer.names import HEDGING, POPULARITY_CACHE, UPDATE_INTERVAL
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

# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [1], HEDGING: [True]}, historical_data, trading_volumes)
simulate_rebalancing_target_ratios.append(
    dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [7], HEDGING: [True]}, historical_data, trading_volumes)
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [14], HEDGING: [True]}, historical_data, trading_volumes)
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [30], HEDGING: [True]}, historical_data, trading_volumes)
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [7], POPULARITY_CACHE: [7], HEDGING: [True]}, historical_data, trading_volumes)
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [14], POPULARITY_CACHE: [14], HEDGING: [True]}, historical_data, trading_volumes)
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [30], POPULARITY_CACHE: [30], HEDGING: [True]}, historical_data, trading_volumes)
simulate_equal_target_ratios.append(
    dex_exp, blocks, {UPDATE_INTERVAL: [None], POPULARITY_CACHE: [None], HEDGING: [True]}, historical_data, trading_volumes)


# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [1], HEDGING: [False]}, historical_data, trading_volumes)
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [7], HEDGING: [False]}, historical_data, trading_volumes)
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [14], HEDGING: [False]}, historical_data, trading_volumes)
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [30], HEDGING: [False]}, historical_data, trading_volumes)
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [7], POPULARITY_CACHE: [7], HEDGING: [False]}, historical_data, trading_volumes)
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [14], POPULARITY_CACHE: [14], HEDGING: [False]}, historical_data, trading_volumes)
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [30], POPULARITY_CACHE: [30], HEDGING: [False]}, historical_data, trading_volumes)
# simulate_equal_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [None], POPULARITY_CACHE: [None], HEDGING: [False]}, historical_data, trading_volumes)
