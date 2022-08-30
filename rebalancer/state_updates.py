from multiprocessing.dummy import Pool
from rebalancer.actions import swap, provide_liquidity, remove_liquidity
from rebalancer.names import ACTION_SWAP, ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION, PROFIT, ARGUMENTS, POOL, BLOCK, POPULARITY, TRADING_VOLUME
from rebalancer import formulas
from rebalancer.policies import SWAP_MEAN
import numpy as np
import math
import copy

rebalancer_actions = {
    ACTION_SWAP: swap,
    ACTION_PROVIDE_LIQUIDITY: provide_liquidity,
    ACTION_REMOVE_LIQUIDITY: remove_liquidity,
}


def get_pool_state_upadate(user_record: dict):
    def state_update(_g, step, sH, s, input):
        pool = copy.deepcopy(s[POOL])
        print("Update: ", input[ACTION], input[ARGUMENTS])
        action = input[ACTION]
        if action in rebalancer_actions:
            return (POOL, rebalancer_actions[action](
                pool, user_record, *input[ARGUMENTS]))
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
        profit[user_type] += formulas.get_price_impact_loss(
            a_in, t_in, t_out)
    return (PROFIT, profit)


TX_PER_DAY = 100


def get_popularity_update(historical_data):
    def popularity_update(_g, step, sH, s, input):
        popularity = copy.deepcopy(s[POPULARITY])
        t = s[BLOCK] / 200
        floor = math.floor(t)
        popularity_sum = sum(
            [ph.iloc[floor].total_volume for ph in historical_data.values()])
        for name, ph in historical_data.items():
            popularity[name] = ph.iloc[floor].total_volume / popularity_sum
        return (POPULARITY, popularity)

    return popularity_update


def get_price_update(historical_data):
    def price_update(_g, step, sH, s, input):
        pool = copy.deepcopy(s[POOL])
        t = s[BLOCK] / TX_PER_DAY
        floor = math.floor(t)
        ceil = floor + 1
        for name, ph in historical_data.items():
            pool[name].price = np.interp(
                t, [floor, ceil], ph[floor:ceil+1].price)
        return (POOL, pool)

    return price_update


def trading_volume_update(_g, step, sH, s, input):
    if s[BLOCK] % 200 == 0:
        trading_volume = {name: {} for name in s[POOL].keys()}
        for t_in, volume in trading_volume.items():
            for t_out in trading_volume.keys():
                if t_out != t_in:
                    volume[t_out] = s[POPULARITY][t_in] * \
                        s[POPULARITY][t_out] * TX_PER_DAY * SWAP_MEAN
        print(trading_volume)
        return (TRADING_VOLUME, trading_volume)
    else:
        return (TRADING_VOLUME, s[TRADING_VOLUME])
