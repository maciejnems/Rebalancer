from rebalancer.names import ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION_SWAP, ACTION, ARGUMENTS, BLOCK, POOL
from rebalancer import formulas
import random
import numpy as np

MIN_PROFIT = 20
ACTIONS = [ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION_SWAP]
PROB = [6, 4, 90]
LIQUIDITY_MEAN = 10000
LIQUIDITY_SPREAD = 4000


def provide_liquidity(users, tokens):
    token = random.choice(list(tokens.values()))
    a_in = np.random.normal(LIQUIDITY_MEAN, LIQUIDITY_SPREAD) / token.price
    user = f'user-{len(users)}'
    users[user] = {token.name: a_in}
    return [a_in, token.name, user]


def remove_liquidity(users, tokens):
    if len(users) == 0:
        return [10, "USDC", "dummy"]
    user = random.choice(list(users.keys()))
    token = [v for v in users.pop(user).items()][0]
    return [token[0], token[1], user]


def get_user_policy():
    users = {}

    def user_policy(_g, step, sH, s):
        print("Step: ", s[BLOCK])
        action = random.choices(ACTIONS, weights=PROB, k=1)[0]
        if action is ACTION_PROVIDE_LIQUIDITY:
            return {ACTION: ACTION_PROVIDE_LIQUIDITY, ARGUMENTS: provide_liquidity(users, s[POOL])}
        elif action is ACTION_REMOVE_LIQUIDITY:
            return {ACTION: ACTION_REMOVE_LIQUIDITY, ARGUMENTS: remove_liquidity(users, s[POOL])}
        else:
            return {ACTION: None}
    return user_policy


def user_policy(_g, step, sH, s):
    print("Step: ", s[BLOCK])
    if s[BLOCK] == 0:
        return {ACTION: ACTION_PROVIDE_LIQUIDITY, ARGUMENTS: [50.0, "USDC", "some user"]}
    elif s[BLOCK] <= 4:
        return {ACTION: ACTION_REMOVE_LIQUIDITY, ARGUMENTS: [10.0, "USDC", "some user"]}
    elif s[BLOCK] == 5:
        return {ACTION: ACTION_REMOVE_LIQUIDITY, ARGUMENTS: [None, "USDC", "some user"]}
    return {ACTION: None}
