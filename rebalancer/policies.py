from rebalancer.names import ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION_SWAP, ACTION, ARGUMENTS, BLOCK, POOL, PROFIT, ARBITRAGEUR_PROFIT, NORMAL_PROFIT, POPULARITY
from rebalancer import formulas
import random
import numpy as np

MIN_PROFIT = 20
ACTIONS = [ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION_SWAP]
PROB = [6, 4, 90]

# Distribution of liquidity providing and swaps based on fiat
LIQUIDITY_MEAN = 10000
LIQUIDITY_SPREAD = 5000
SWAP_MEAN = 1000
SWAP_SPREAD = 500


def best_arbitrage(tokens):
    TB = formulas.target_balances(tokens)

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

    profit = (1 - formulas.SWAP_FEE) * (a_out - a_in * (in_token.price / out_token.price)) * \
        out_token.price

    return a_in, in_token.name, out_token.name, profit


def get_arbitrage(tokens):
    a_in, in_token, out_token, profit = best_arbitrage(tokens)
    if profit > 20:
        return [a_in, in_token, out_token]
    else:
        return None


def random_swap_tokens(tokens, popularity=None):
    swapped = []
    if popularity is None:
        swapped = random.sample(list(tokens.keys()), 2)
    else:
        (names, prob) = zip(*popularity.items())
        swapped = np.random.choice(names,  2, p=prob, replace=False)
    t_in, t_out = tokens[swapped[0]], tokens[swapped[1]]
    a_in = np.random.normal(SWAP_MEAN, SWAP_SPREAD) / t_in.price
    return [a_in, t_in.name, t_out.name]


def random_provide_liquidity(users, tokens, popularity=None):
    token = None
    if popularity is None:
        name =  random.choice(list(tokens.keys()))
    else:
        (names, prob) = zip(*popularity.items())
        name = np.random.choice(names,  p=prob)
    token = tokens[name]
    a_in = np.random.normal(LIQUIDITY_MEAN, LIQUIDITY_SPREAD) / token.price
    user = f'user-{len(users)}'
    users[user] = {token.name: a_in}
    return [a_in, token.name, user]


def random_remove_liquidity(users, tokens):
    if len(users) == 0:
        return [10, "USDC", "dummy"]
    user = random.choice(list(users.keys()))
    token = [v for v in users.pop(user).items()][0]
    return [token[0], token[1], user]


def get_user_policy():
    users = {}

    def user_policy(_g, step, sH, s):
        print("Step: ", s[BLOCK], s[POOL])
        action = random.choices(ACTIONS, weights=PROB, k=1)[0]
        if action is ACTION_PROVIDE_LIQUIDITY:
            return {ACTION: ACTION_PROVIDE_LIQUIDITY, ARGUMENTS: random_provide_liquidity(users, s[POOL], s[POPULARITY])}
        elif action is ACTION_REMOVE_LIQUIDITY:
            return {ACTION: ACTION_REMOVE_LIQUIDITY, ARGUMENTS: random_remove_liquidity(users, s[POOL])}
        elif action is ACTION_SWAP:
            arbitrage = get_arbitrage(s[POOL])
            if arbitrage is not None:
                print("ARBITRAGE OPORTUNITY")
                if random.random() < 0.6:
                    print("ARBITRAGE")
                    return {ACTION: ACTION_SWAP, ARGUMENTS: arbitrage, PROFIT: ARBITRAGEUR_PROFIT}
            print("RANDOM swap")
            return {ACTION: ACTION_SWAP, ARGUMENTS: random_swap_tokens(s[POOL], s[POPULARITY]), PROFIT: NORMAL_PROFIT}
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
