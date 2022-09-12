from multiprocessing.dummy import Pool
from rebalancer.actions import swap, provide_liquidity, remove_liquidity, rebalance
from rebalancer.names import ACTION_SWAP, ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION, PROFIT, ARGUMENTS, POOL, POPULARITY, TRADING_VOLUME, MAX_HISTORY, ARBITRAGEUR_PROFIT, NORMAL_PROFIT, BLOCK
from rebalancer import formulas
from rebalancer.policies import SWAP_MEAN, best_provide_liquidity
import numpy as np
import math
import copy

rebalancer_actions = {
    ACTION_SWAP: swap,
    ACTION_PROVIDE_LIQUIDITY: provide_liquidity,
    ACTION_REMOVE_LIQUIDITY: remove_liquidity,
}


def prune_state_history(_g, step, sH, s, input):
    if len(sH) > s[MAX_HISTORY]:
        sH.pop(0)
    return (MAX_HISTORY, s[MAX_HISTORY])


def get_pool_state_upadate(user_record: dict, historical_data, should_rebalance):
    def state_update(_g, step, sH, s, input):
        pool = copy.deepcopy(s[POOL])
        # Make actions
        if s[BLOCK] % (TX_PER_DAY * UPDATE_INTERVAL) == 2:
            if should_rebalance:
                pool = rebalance(s[POOL], user_record,
                                 s[TRADING_VOLUME], "root")
        else:
            action = input[ACTION]
            if action in rebalancer_actions:
                pool = rebalancer_actions[action](
                    pool, user_record, *input[ARGUMENTS])

        # Update prices
        t = s[BLOCK] / TX_PER_DAY
        floor = math.floor(t)
        ceil = floor + 1
        for name, ph in historical_data.items():
            pool[name].price = np.interp(
                t, [floor, ceil], ph[floor:ceil+1].price)
        else:
            return (POOL, pool)

    return state_update


def block_update(_g, step, sH, s, input):
    return (BLOCK, s[BLOCK] + 1)


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
UPDATE_INTERVAL = 1
MAX_HISTORY_CACHE = 7


def get_popularity_update(historical_data):
    def popularity_update(_g, step, sH, s, input):
        if s[BLOCK] % TX_PER_DAY == 0:
            popularity = copy.deepcopy(s[POPULARITY])
            t = math.floor(s[BLOCK] / TX_PER_DAY)
            popularity_sum = sum(
                [ph.iloc[t].total_volume for ph in historical_data.values()])
            for name, ph in historical_data.items():
                popularity[name] = ph.iloc[t].total_volume / popularity_sum
            return (POPULARITY, popularity)
        else:
            return (POPULARITY, s[POPULARITY])

    return popularity_update


def trading_volume_update(_g, step, sH, s, input):
    if s[BLOCK] % (TX_PER_DAY * UPDATE_INTERVAL) == 1:
        trading_volume = {
            name: {t: 0 for t in s[POOL].keys() if t != name} for name in s[POOL].keys()}
        for sh in sH[-TX_PER_DAY * MAX_HISTORY_CACHE::TX_PER_DAY]:
            for t_in, volume in trading_volume.items():
                for t_out in trading_volume.keys():
                    if t_out != t_in:
                        volume[t_out] += sh[0][POPULARITY][t_in] * \
                            sh[0][POPULARITY][t_out] / \
                            (1 - sh[0][POPULARITY][t_in]) * \
                            TX_PER_DAY * SWAP_MEAN
        for t_in, volume in trading_volume.items():
            for t_out in trading_volume.keys():
                if t_out != t_in:
                    volume[t_out] /= len(sH[-TX_PER_DAY *
                                         MAX_HISTORY_CACHE::TX_PER_DAY])
        # for t_in, volume in trading_volume.items():
        #     for t_out in trading_volume.keys():
        #         if t_out != t_in:
        #             volume[t_out] = s[POPULARITY][t_in] * \
        #                 s[POPULARITY][t_out] / (1 - s[POPULARITY][t_in]) * TX_PER_DAY * SWAP_MEAN
        return (TRADING_VOLUME, trading_volume)
    else:
        return (TRADING_VOLUME, s[TRADING_VOLUME])
