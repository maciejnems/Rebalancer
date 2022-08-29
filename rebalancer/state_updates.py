from multiprocessing.dummy import Pool
from rebalancer.actions import swap, provide_liquidity, remove_liquidity
from rebalancer.names import ACTION_SWAP, ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION, PROFIT, ARGUMENTS, POOL, BLOCK, POPULARITY
from rebalancer import formulas
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
