from multiprocessing.dummy import Pool
from rebalancer.actions import swap, provide_liquidity, remove_liquidity
from rebalancer.formulas import compute_C
from rebalancer.names import ACTION_SWAP, ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION, ARGUMENTS, POOL, BLOCK

rebalancer_actions = {
    ACTION_SWAP: swap,
    ACTION_PROVIDE_LIQUIDITY: provide_liquidity,
    ACTION_REMOVE_LIQUIDITY: remove_liquidity,
}


def get_pool_state_upadate(user_record: dict):
    def state_update(_g, step, sH, s, input):
        print("Input", input)
        action = input[ACTION]
        if action in rebalancer_actions:
            result = rebalancer_actions[action](
                s[POOL], user_record, *input[ARGUMENTS])
            print("Result", result, user_record)
            return (POOL, result)
        else:
            return (POOL, s[POOL])

    return state_update


def block_update(_g, step, sH, s, input):
    return (BLOCK, s[BLOCK] + 1)
