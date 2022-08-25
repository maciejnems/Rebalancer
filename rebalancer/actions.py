from rebalancer import formulas
from rebalancer.model import Token


def swap(state, user_register, a_in: float, t_in: str, t_out: str):
    a_out = formulas.amount_out(a_in, state[t_in], state[t_out]) * 0.95
    state[t_in].balance += a_in
    state[t_out].balance -= a_out
    return state


def provide_liquidity(state, user_register, deposit: float, name: str, user: str):
    C = formulas.compute_C(state)
    supply = formulas.get_issued(name, deposit, C, state)
    state[name].supply += supply
    target_ratios = formulas.new_target_ratios(
        name, deposit, C, state)
    if user not in user_register:
        user_register[user] = {}
    if name in user_register[user]:
        user_register[user][name] += supply
    else:
        user_register[user][name] = supply
    state[name].balance += deposit
    for name, tr in target_ratios.items():
        state[name].target_ratio = tr
    return state


def remove_liquidity(state, user_register, redeemed: float, name: str, user: str):
    if user not in user_register or name not in user_register[user]:
        print(f"No entry for user {user} for token {name}")
        return state
    if redeemed is None:
        redeemed = user_register[user][name]
    if user_register[user][name] < redeemed:
        print(f"User does not have enough founds. Tried to withdraw {redeemed}, has {user_register[user][name]}")
        return state
    C = formulas.compute_C(state)
    withdrawal = formulas.get_withdrawal(name, redeemed, C, state)
    if withdrawal > state[name].balance:
        print(f"Not enough tokens to withdraw {withdrawal} of token {name}")
        return state
    state[name].supply -= redeemed
    user_register[user][name] -= redeemed
    state[name].balance -= withdrawal
    target_ratios = formulas.new_target_ratios(
        name, -withdrawal, C, state)
    for name, tr in target_ratios.items():
        state[name].target_ratio = tr
    return state
