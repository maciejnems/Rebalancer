from rebalancer.actions import swap, provide_liquidity, remove_liquidity, rebalance, compensate
from rebalancer.names import ACTION_SWAP, ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION, HEDGING, PROFIT, ARGUMENTS, POOL, POPULARITY, TRADING_VOLUME, MAX_HISTORY, TIMESTAMP, POPULARITY_CACHE, UPDATE_INTERVAL
from rebalancer import formulas
from rebalancer.policies import SWAP_MEAN
from rebalancer.model import VALUE_PER_TOKEN, Time
import numpy as np
import math
import copy

rebalancer_actions = {
    ACTION_SWAP: swap,
    ACTION_PROVIDE_LIQUIDITY: provide_liquidity,
    ACTION_REMOVE_LIQUIDITY: remove_liquidity,
}


def prune_state_history(_g, step, sH, s, input):
    if sH[-1][0][TIMESTAMP].block != 0:
        sH.pop()
    return (MAX_HISTORY, s[MAX_HISTORY])


def get_pool_state_upadate(user_record: dict, historical_data, should_rebalance):
    def state_update(params, step, sH, s, input):
        pool = copy.deepcopy(s[POOL])
        # Action:
        action = input[ACTION]
        if action in rebalancer_actions:
            pool = rebalancer_actions[action](
                pool, user_record, *input[ARGUMENTS])

        if s[TIMESTAMP].block == 2:
            # Rebalance
            if should_rebalance and (s[TIMESTAMP].day % params[UPDATE_INTERVAL] == 0):
                pool = rebalance(pool, user_record,
                                 s[TRADING_VOLUME], "root")
            # Compensate
            if params[HEDGING]:
                pool = compensate(pool, user_record, "root",
                                  len(historical_data) * VALUE_PER_TOKEN)

        # Update prices
        t = s[TIMESTAMP].day + s[TIMESTAMP].block / s[TIMESTAMP].block_limit
        floor = math.floor(t)
        ceil = floor + 1
        for name, ph in historical_data.items():
            pool[name].price = np.interp(
                t, [floor, ceil], ph[floor:ceil+1].price)
        return (POOL, pool)

    return state_update


def get_timestamp_update(tx_per_day):
    def timestamp_update(_g, step, sH, s, input):
        if s[TIMESTAMP].block + 1 == s[TIMESTAMP].block_limit:
            day = s[TIMESTAMP].day + 1
            return (TIMESTAMP, Time(day, 0, tx_per_day[day]))
        timestamp = copy.deepcopy(s[TIMESTAMP])
        timestamp.block += 1
        return (TIMESTAMP, timestamp)

    return timestamp_update


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


def get_popularity_update(historical_data):
    def popularity_update(_g, step, sH, s, input):
        if s[TIMESTAMP].block == 0:
            popularity = copy.deepcopy(s[POPULARITY])
            day = s[TIMESTAMP].day
            popularity_sum = sum(
                [ph.iloc[day].total_volume for ph in historical_data.values()])
            for name, ph in historical_data.items():
                popularity[name] = ph.iloc[day].total_volume / popularity_sum
            return (POPULARITY, popularity)
        else:
            return (POPULARITY, s[POPULARITY])

    return popularity_update


def get_trading_volume_update():
    trading_volume_history = []

    def trading_volume_update(params, step, sH, s, input):
        if s[TIMESTAMP].block == 1:
            if len(trading_volume_history) > params[POPULARITY_CACHE]:
                trading_volume_history.pop(0)
            trading_volume = {
                name: {} for name in s[POOL].keys()}
            # Trading volume for this day
            all = 0
            for t_in, volume in trading_volume.items():
                for t_out in trading_volume.keys():
                    if t_out != t_in:
                        volume[t_out] = s[POPULARITY][t_in] * s[POPULARITY][t_out] / \
                            (1 - s[POPULARITY][t_in]) * \
                            s[TIMESTAMP].block_limit * SWAP_MEAN
            trading_volume_history.append(trading_volume)
            if s[TIMESTAMP].day % params[UPDATE_INTERVAL] == 0:
                trading_volume = {
                    name: {t: 0 for t in s[POOL].keys() if t != name} for name in s[POOL].keys()}
                for sh in trading_volume_history[:params[POPULARITY_CACHE]]:
                    for t_in, volume in trading_volume.items():
                        for t_out in trading_volume.keys():
                            if t_out != t_in:
                                volume[t_out] += sh[t_in][t_out]
                for t_in, volume in trading_volume.items():
                    for t_out in trading_volume.keys():
                        if t_out != t_in:
                            volume[t_out] /= len(
                                trading_volume_history[:params[POPULARITY_CACHE]])
                return (TRADING_VOLUME, trading_volume)

        return (TRADING_VOLUME, s[TRADING_VOLUME])

    return trading_volume_update
