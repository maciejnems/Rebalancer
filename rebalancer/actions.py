from rebalancer import formulas


def swap(state, user_register, a_in: float, t_in: str, t_out: str):
    # a_out = formulas.amount_out(
    #     a_in, state[t_in], state[t_out]) * (1 - formulas.SWAP_FEE)
    a_out = formulas.amount_out(
        a_in, state[t_in], state[t_out])
    state[t_in].balance += a_in
    state[t_out].balance -= a_out
    return state


def provide_liquidity(state, user_register, deposit: float, name: str, user: str):
    supply = formulas.get_issued(name, deposit, state)
    state[name].supply += supply
    target_ratios = formulas.new_target_ratios(
        name, deposit, state)
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
        print(
            f"User {user} does not have enough founds. Tried to withdraw {redeemed} {name}, has {user_register[user][name]} {name}")
        return state
    withdrawal = formulas.get_withdrawal(name, redeemed, state)
    if withdrawal > state[name].balance:
        print(f"Not enough tokens to withdraw {withdrawal} of token {name}")
        return state
    target_ratios = formulas.new_target_ratios(
        name, -withdrawal, state)
    state[name].supply -= redeemed
    user_register[user][name] -= redeemed
    state[name].balance -= withdrawal
    for name, tr in target_ratios.items():
        state[name].target_ratio = tr
    return state


def rebalance(state, user_register, trading_volumes, user: str):
    wanted_target_ratios = formulas.wanted_target_ratio(state, trading_volumes)
    redeem_ratios = {t.name: (
        wanted_target_ratios[t.name] / t.target_ratio) - 1 for t in state.values()}
    for t, ratio in redeem_ratios.items():
        state = remove_liquidity(
            state, user_register, -state[t].supply * ratio, t, user)
    return state


def compensate(state, user_register, user, genesis_V):
    V = formulas.compute_V(state)
    TB = formulas.target_balances(state)
    ratio = (genesis_V - V) / V
    for t, tb in TB.items():
        state = remove_liquidity(
            state, user_register, -state[t].supply * ratio, t, user)
    return state
