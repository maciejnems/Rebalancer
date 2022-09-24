from lib2to3.pgen2 import token
import math
from rebalancer.names import HEDGING, POPULARITY_CACHE, SWAP, UPDATE_INTERVAL
from cadCAD.configuration import Experiment
from simulations import simulate_equal_target_ratios, simulate_rebalancing_target_ratios
from rebalancer.model import TX_PER_DAY
from rebalancer import utils

dex_exp = Experiment()

# Tokens used for 10 token simulation in paper
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

# Tokens used for 5 token simulation in paper
big_tokens = [
    "usdt",
    "eth",
    "xrp",
    "link",
    "bch",
]


tokens = big_tokens

# All historical data
historical_data = utils.get_historical_data(
    tokens, "2020-09-01 00:00:00 UTC", "2022-09-01 00:00:00 UTC")

# During dogecoin - everything before 07.2021
# historical_data = utils.get_historical_data(
#     tokens, "2020-09-01 00:00:00 UTC", "2021-07-01 00:00:00 UTC")

# After dogecoin - everything after 07.2021
# historical_data = utils.get_historical_data(
#     tokens, "2021-07-01 00:00:00 UTC", "2022-09-01 00:00:00 UTC")

# Short - is for testing
historical_data = utils.get_historical_data(
    tokens, "2022-08-22 00:00:00 UTC", "2022-08-25 00:00:00 UTC")

days = len(next(iter(historical_data.values()))) - 1
blocks = TX_PER_DAY * days

blocks, trading_volumes = utils.get_tx_per_day(historical_data, blocks)

print("Simulating...")
print("average tx per day:", TX_PER_DAY)
print("max tx per day:", max(trading_volumes))
print("min tx per day:", min(trading_volumes))
print("days:", days)
print("blocks:", blocks)

### Folowing are scenarios tested in the paper. Uncomment any of them to run.

### Used for test without hedging
# simulate_equal_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [None], POPULARITY_CACHE: [None], HEDGING: [False], SWAP: [5000]}, historical_data, trading_volumes)
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [7], HEDGING: [False], SWAP: [5000]}, historical_data, trading_volumes)


### Used for tests with hedging
# simulate_equal_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [None], POPULARITY_CACHE: [None], HEDGING: [True], SWAP: [5000]}, historical_data, trading_volumes)
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [7], HEDGING: [True], SWAP: [5000]}, historical_data, trading_volumes)

### Simulation by trading value
# for i in range(1, 21):
#     simulate_rebalancing_target_ratios.append(
#         dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [7], HEDGING: [True], SWAP: [i*1000]}, historical_data, trading_volumes)
#     simulate_equal_target_ratios.append(
#         dex_exp, blocks, {UPDATE_INTERVAL: [None], POPULARITY_CACHE: [None], HEDGING: [True], SWAP: [i*1000]}, historical_data, trading_volumes)

### Simulation by cache size
# simulate_equal_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [None], POPULARITY_CACHE: [None], HEDGING: [True], SWAP: [5000]}, historical_data, trading_volumes)
# for i in range(1, 31):
#     simulate_rebalancing_target_ratios.append(
#         dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [i], HEDGING: [True], SWAP: [5000]}, historical_data, trading_volumes)


### Simulation by update interval size
# interval = sorted({2 ** (i/9) for i in range(1, 87)})
# simulate_equal_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [None], POPULARITY_CACHE: [None], HEDGING: [True], SWAP: [5000]}, historical_data, trading_volumes)
# for i in interval:
#     simulate_rebalancing_target_ratios.append(
#         dex_exp, blocks, {UPDATE_INTERVAL: [i], POPULARITY_CACHE: [7], HEDGING: [True], SWAP: [5000]}, historical_data, trading_volumes)


### Simulate 5 with different weights for Balancer
### This works only for big_tokens dataset
# simulate_equal_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [None], POPULARITY_CACHE: [None], HEDGING: [True], SWAP: [5000]}, historical_data, trading_volumes)
# simulate_equal_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [None], POPULARITY_CACHE: [None], HEDGING: [True], SWAP: [5000]}, historical_data, trading_volumes, target_ratios={
#         "eth": 0.3,
#         "usdt": 0.3,
#         "xrp": 0.4/3,
#         "link": 0.4/3,
#         "bch": 0.4/3
#     })
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [1], POPULARITY_CACHE: [7], HEDGING: [True], SWAP: [5000]}, historical_data, trading_volumes)
# simulate_rebalancing_target_ratios.append(
#     dex_exp, blocks, {UPDATE_INTERVAL: [750], POPULARITY_CACHE: [7], HEDGING: [True], SWAP: [5000]}, historical_data, trading_volumes)
