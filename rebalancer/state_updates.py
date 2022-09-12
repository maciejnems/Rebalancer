from multiprocessing.dummy import Pool
from rebalancer.actions import swap, provide_liquidity, remove_liquidity, rebalance
from rebalancer.names import ACTION_SWAP, ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION, PROFIT, ARGUMENTS, POOL, POPULARITY, TRADING_VOLUME, MAX_HISTORY, ARBITRAGEUR_PROFIT, NORMAL_PROFIT, REBALANCE, TIME
from rebalancer import formulas
from rebalancer.policies import SWAP_MEAN, best_provide_liquidity
from rebalancer.model import Time
import numpy as np
import math
import copy

rebalancer_actions = {
    ACTION_SWAP: swap,
    ACTION_PROVIDE_LIQUIDITY: provide_liquidity,
    ACTION_REMOVE_LIQUIDITY: remove_liquidity,
}

prev_profit = {
    ARBITRAGEUR_PROFIT: [0, 0, 0, 0],
    NORMAL_PROFIT: [0, 0, 0, 0],
}

loss = [0]


def prune_state_history(_g, step, sH, s, input):
    if len(sH) > s[MAX_HISTORY]:
        sH.pop(0)
    return (MAX_HISTORY, s[MAX_HISTORY])


def get_pool_state_upadate(user_record: dict, historical_data):
    def state_update(_g, step, sH, s, input):
        pool = copy.deepcopy(s[POOL])
        # Make actions
        if s[TIME].block == 2:
            if s[REBALANCE]:
                pool = rebalance(s[POOL], user_record,
                                 s[TRADING_VOLUME], "root")
            # print({t.name: t.target_ratio for t in pool.values()})
        else:
            before = formulas.compute_V(pool)
            # print("Update: ", s[REBALANCE], input[ACTION], input[ARGUMENTS])
            # print("STATE: ", {name: (t.balance, t.target_ratio) for name, t in s[POOL].items()})
            # print("Target ratios: ", formulas.wanted_target_ratio(s[POOL], s[TRADING_VOLUME]))
            # print("Target Balance: ", formulas.target_balances(s[POOL]))
            action = input[ACTION]
            if action in rebalancer_actions:
                pool = rebalancer_actions[action](
                    pool, user_record, *input[ARGUMENTS])
            after = formulas.compute_V(pool)
            loss[0] += after - before

            # print("Pool", s[REBALANCE], before - after)

        # Update prices
        t = s[TIME].block / s[TIME].block_limit
        for name, ph in historical_data.items():
            # print(t,  s[TIME].day, ph[s[TIME].day:s[TIME].day+2].price)
            pool[name].price = np.interp(
                t, [0, 1], ph[s[TIME].day:s[TIME].day+2].price)
        return (POOL, pool)

    return state_update


# def get_block_update(trading_volumes):
#     def block_update(_g, step, sH, s, input):
#         if s[BLOCK] + 1 == trading_volumes.iloc[s[DAY]]:
#             return (BLOCK, 0)
#         return (BLOCK, s[BLOCK] + 1)

#     return block_update


def profit_update(_g, step, sH, s, input):
    profit = copy.deepcopy(s[PROFIT])
    if input[ACTION] is ACTION_SWAP:
        a_in, t_in, t_out = input[ARGUMENTS]
        t_in = s[POOL][t_in]
        t_out = s[POOL][t_out]
        user_type = input[PROFIT]
        profit[user_type][0] += 1
        diff = formulas.get_price_impact_loss(
            a_in, t_in, t_out)
        if diff < 0:
            profit[user_type][1] += diff
        else:
            profit[user_type][2] += diff
    return (PROFIT, profit)


TX_PER_DAY = 200
UPDATE_INTERVAL = 7
MAX_HISTORY_CACHE = 14


# def print_profit(s, user):
#     print(s[REBALANCE], s[BLOCK], loss[0],  user, s[PROFIT][user][0] - prev_profit[user][0],
#           s[PROFIT][user][1] -
#           prev_profit[user][1],
#           s[PROFIT][user][2] -
#           prev_profit[user][2],
#           (s[PROFIT][user][1] + s[PROFIT][user][2] - prev_profit[user][3]) / (s[PROFIT][user][0] - prev_profit[user][0]), formulas.compute_V(s[POOL]))
#     prev_profit[user][0] = s[PROFIT][user][0]
#     prev_profit[user][1] = s[PROFIT][user][1]
#     prev_profit[user][2] = s[PROFIT][user][2]
#     prev_profit[user][3] = s[PROFIT][user][1] + \
#         s[PROFIT][user][2]


def get_popularity_update(historical_data):
    def popularity_update(_g, step, sH, s, input):
        if s[TIME].block == 0:
            # print_profit(s, ARBITRAGEUR_PROFIT)
            # if s[BLOCK] > 0:
            #     print_profit(s, NORMAL_PROFIT)
            popularity = copy.deepcopy(s[POPULARITY])
            day = s[TIME].day
            popularity_sum = sum(
                [ph.iloc[day].total_volume for ph in historical_data.values()])
            for name, ph in historical_data.items():
                popularity[name] = ph.iloc[day].total_volume / popularity_sum
            return (POPULARITY, popularity)
        else:
            return (POPULARITY, s[POPULARITY])

    return popularity_update


def get_time_update(trading_volumes):

    def time_update(_g, step, sH, s, input):
        # print("block", s[TIME])
        if s[TIME].block + 1 == s[TIME].block_limit:
            day = s[TIME].day + 1
            return (TIME, Time(day, 0, trading_volumes.iloc[day]))
            
        time = copy.deepcopy(s[TIME])
        time.block += 1
        return (TIME, time)

    return time_update


# def get_price_update(historical_data):
#     def price_update(_g, step, sH, s, input):
#         pool = copy.deepcopy(s[POOL])
#         t = s[BLOCK] / TX_PER_DAY
#         floor = math.floor(t)
#         ceil = floor + 1
#         for name, ph in historical_data.items():
#             pool[name].price = np.interp(
#                 t, [floor, ceil], ph[floor:ceil+1].price)
#         return (POOL, pool)

#     return price_update


def trading_volume_update(_g, step, sH, s, input):
    if s[TIME].block == 1:
        trading_volume = {
            name: {t: 0 for t in s[POOL].keys() if t != name} for name in s[POOL].keys()}
        # for sh in sH[-TX_PER_DAY * MAX_HISTORY_CACHE::TX_PER_DAY]:
        #     for t_in, volume in trading_volume.items():
        #         for t_out in trading_volume.keys():
        #             if t_out != t_in:
        #                 volume[t_out] += sh[0][POPULARITY][t_in] * \
        #                     sh[0][POPULARITY][t_out] / \
        #                     (1 - sh[0][POPULARITY][t_in]) * \
        #                     TX_PER_DAY * SWAP_MEAN
        # print([x[BLOCK] for x in sh])
        # for t_in, volume in trading_volume.items():
        #     for t_out in trading_volume.keys():
        #         if t_out != t_in:
        #             volume[t_out] = s[POPULARITY][t_in] * \
        #                 s[POPULARITY][t_out] * TX_PER_DAY * SWAP_MEAN
        # for t_in, volume in trading_volume.items():
        #     for t_out in trading_volume.keys():
        #         if t_out != t_in:
        #             volume[t_out] /= len(sH[-TX_PER_DAY *
        #                                  MAX_HISTORY_CACHE::TX_PER_DAY])
        # print("trading volume update", len(sH[-TX_PER_DAY * MAX_HISTORY_CACHE::TX_PER_DAY]))
        # print(s[POPULARITY])
        # print(sum([sum([v for v in t.values()])for t in trading_volume.values()]))
        for t_in, volume in trading_volume.items():
            for t_out in trading_volume.keys():
                if t_out != t_in:
                    volume[t_out] = s[POPULARITY][t_in] * \
                        s[POPULARITY][t_out] * s[TIME].block_limit * SWAP_MEAN 
        return (TRADING_VOLUME, trading_volume)
    else:
        return (TRADING_VOLUME, s[TRADING_VOLUME])
