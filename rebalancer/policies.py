from rebalancer.names import ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION_SWAP, ACTION, ARGUMENTS, BLOCK, POOL
from rebalancer import formulas
import random
import numpy as np

MIN_PROFIT = 20
ACTIONS = [ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION_SWAP]
PROB = [6, 4, 90]
LIQUIDITY_MEAN = 10000
LIQUIDITY_SPREAD = 4000


def best_arbitrage(tokens):
    C = formulas.compute_C(tokens)
    TB = formulas.target_balances(C, tokens)

    differences = {name: tokens[name].price *
                   (TB[name] - tokens[name].balance) for name in tokens}
    in_token, out_token = tokens[max(differences, key=differences.get)], tokens[min(
        differences, key=differences.get)]
    a_in = TB[in_token.name] - in_token.balance
    a_out = out_token.balance - TB[out_token.name]

    if formulas.amount_out(a_in, in_token, out_token) > a_out:
        a_in = formulas.amount_in(a_out, in_token, out_token)
    else:
        a_out = formulas.amount_out(a_in, in_token, out_token)

    profit = (a_out - a_in * (in_token.price / out_token.price)) * \
        out_token.price

    return a_in, in_token.name, out_token.name, profit


def get_arbitrage(tokens):
    a_in, in_token, out_token, profit = best_arbitrage(tokens)
    if profit > 20:
        return [a_in, in_token, out_token]
    else:
        return None


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
        elif action is ACTION_SWAP:
            arbitrage = get_arbitrage(s[POOL])
            if arbitrage is not None:
                print("ARBITRAGE OPORTUNITY")
                return {ACTION: ACTION_SWAP, ARGUMENTS: arbitrage}
            else:
                print("simple swap")
                return {ACTION: ACTION_SWAP, ARGUMENTS: [1000.0, "USDC", "USDT"]}
        else:
            return {}
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
