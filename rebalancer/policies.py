from rebalancer.names import ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION_SWAP, ACTION, ARGUMENTS, BLOCK, POOL, PROFIT, ARBITRAGEUR_PROFIT, NORMAL_PROFIT, POPULARITY, TRADING_VOLUME
from rebalancer import formulas
import random
import numpy as np

MIN_PROFIT = 20
ACTIONS = [ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION_SWAP]
PROB = [16, 4, 80]

# Distribution of liquidity providing and swaps based on fiat
LIQUIDITY_MEAN = 10000
LIQUIDITY_SPREAD = 5000
SWAP_MEAN = 1000
SWAP_SPREAD = 500
MIN_ARBITRAGE_SWAP_PROFIT = 20
MIN_INTENTIONAL_DEPOSIT = 1000
INTENTIONAL_LIQUIDITY_MEAN = 20000
INTENTIONAL_LIQUIDITY_SPREAD = 5000


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
    if profit > MIN_ARBITRAGE_SWAP_PROFIT:
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


def best_provide_liquidity(tokens, trading_volumes):
    wanted_target_ratio = formulas.wanted_target_ratio(tokens, trading_volumes)
    token_profit = {token.name: wanted_target_ratio[token.name] -
                    token.target_ratio for token in tokens.values()}
    best_profit = max(token_profit, key=token_profit.get)
    diff = formulas.deposit_to_change_ratio(
        best_profit, wanted_target_ratio[best_profit], tokens)
    if diff > MIN_INTENTIONAL_DEPOSIT:
        diff = max(diff, np.random.normal(
            INTENTIONAL_LIQUIDITY_MEAN, INTENTIONAL_LIQUIDITY_SPREAD)) / tokens[best_profit].price
        print("BEST PROVIDE LIQUIDITY: ", diff, best_profit)
        return [diff, best_profit]
    return None


def random_provide_liquidity(tokens, popularity=None):
    token = None
    if popularity is None:
        name = random.choice(list(tokens.keys()))
    else:
        (names, prob) = zip(*popularity.items())
        name = np.random.choice(names,  p=prob)
    token = tokens[name]
    a_in = np.random.normal(LIQUIDITY_MEAN, LIQUIDITY_SPREAD) / token.price
    return [a_in, token.name]


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
            deposit = best_provide_liquidity(s[POOL], s[TRADING_VOLUME])
            if deposit is None:
                deposit = random_provide_liquidity(s[POOL], s[POPULARITY])
            user = f'user-{len(users)}'
            deposit.append(user)
            users[user] = {deposit[1]: deposit[0]}
            return {ACTION: ACTION_PROVIDE_LIQUIDITY, ARGUMENTS: deposit}
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
