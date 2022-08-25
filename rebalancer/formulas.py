from rebalancer.model import Token
import math


def amount_out(a_in: float, t_in: Token, t_out: Token) -> float:
    return t_out.balance * \
        (1-math.pow(t_in.balance / (t_in.balance +
         a_in), t_in.target_ratio / t_out.target_ratio))


def target_balance_denominator(tokens: dict) -> float:
    return math.prod(math.pow(t.target_ratio/t.price, t.target_ratio) for t in tokens.values())


def target_balances(C: float, tokens: dict) -> dict:
    prod = target_balance_denominator(tokens)
    return {t.name: (t.target_ratio * C / t.price) / prod for t in tokens.values()}


def target_balance(name: str, C: float, tokens: dict) -> float:
    TB = tokens[name].target_ratio * C / tokens[name].price
    print(TB)
    prod = target_balance_denominator(tokens)
    print(prod)
    return TB / prod


def new_target_ratios(name: str, diff: float, C: float, tokens: dict) -> dict:
    TB = target_balance(name, C, tokens)
    multiplier = TB / (TB + diff * tokens[name].target_ratio)
    ratios = {t.name: t.target_ratio *
              multiplier for t in tokens.values() if t.name is not name}
    ratios[name] = tokens[name].target_ratio * (1 + diff/TB) * multiplier
    return ratios


def compute_C(tokens: dict) -> float:
    return math.prod(math.pow(t.balance, t.target_ratio) for t in tokens.values())


#             Deposit_i * Supply_i   
# P_issued = ----------------------
#                      TB_i
def get_issued(name: str, deposit: float, C: float, tokens: dict) -> float:
    TB = target_balance(name, C, tokens)
    return deposit * tokens[name].supply / TB


#               P_redeemed * TB_i   
# Withdraw_i = -------------------
#                    Supply_i
def get_withdrawal(name: str, redeemed: float, C: float, tokens: dict) -> float:
    TB = target_balance(name, C, tokens)
    return redeemed * TB / tokens[name].supply

