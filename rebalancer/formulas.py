from rebalancer.model import Token
import math

SWAP_FEE = 0.05


def amount_out(a_in: float, t_in: Token, t_out: Token) -> float:
    return t_out.balance * \
        (1-math.pow(t_in.balance / (t_in.balance +
         a_in), t_in.target_ratio / t_out.target_ratio))


def amount_in(a_out: float, t_in: Token, t_out: Token) -> float:
    return t_in.balance * \
        (math.pow(t_out.balance / (t_out.balance -
         a_out), t_out.target_ratio / t_in.target_ratio)-1)


def _target_balance_denominator(tokens: dict) -> float:
    return math.prod(math.pow(t.target_ratio/t.price, t.target_ratio) for t in tokens.values())


def _compute_C(tokens: dict) -> float:
    return math.prod(math.pow(t.balance, t.target_ratio) for t in tokens.values())


def compute_V(tokens: dict) -> float:
    return sum([t.balance * t.price for t in tokens.values()])


def target_balances(tokens: dict) -> dict:
    C = _compute_C(tokens)
    prod = _target_balance_denominator(tokens)
    return {t.name: (t.target_ratio * C / t.price) / prod for t in tokens.values()}


def target_balance(name: str, tokens: dict) -> float:
    TB = target_balances(tokens)
    return TB[name]


def new_target_ratios(name: str, diff: float, tokens: dict) -> dict:
    TB = target_balance(name, tokens)
    multiplier = TB / (TB + diff * tokens[name].target_ratio)
    ratios = {t.name: t.target_ratio *
              multiplier for t in tokens.values() if t.name is not name}
    ratios[name] = tokens[name].target_ratio * (1 + diff/TB) * multiplier
    return ratios


def deposit_to_change_ratio(name: str, wanted_ratio: float, tokens: dict):
    TB = target_balance(name, tokens)
    diff = (wanted_ratio /
            (tokens[name].target_ratio) - 1) * TB / (1-wanted_ratio)
    return diff


def wanted_target_ratio(tokens: dict, trading_volumes: dict):
    target_ratios = {}
    numerators = {i: math.sqrt(sum([trading_volumes[i][j] + trading_volumes[j][i]
                               for j in tokens.keys() if j != i])) for i in tokens.keys()}
    # In this implementation trading_volumes already are V_i,j * P_i, so no need for squaring price like in paper
    # numerators = {i: math.sqrt(sum([tokens[i].price * trading_volumes[i][j] + tokens[j].price *
    #                            trading_volumes[j][i] for j in tokens.keys() if j != i])) for i in tokens.keys()}
    denominator = sum(numerators.values())
    target_ratios = {name: numerator /
                     denominator for name, numerator in numerators.items()}
    return target_ratios


#             Deposit_i * Supply_i
# P_issued = ----------------------
#                      TB_i
def get_issued(name: str, deposit: float, tokens: dict) -> float:
    TB = target_balance(name, tokens)
    return deposit * tokens[name].supply / TB


#               P_redeemed * TB_i
# Withdraw_i = -------------------
#                    Supply_i
def get_withdrawal(name: str, redeemed: float, tokens: dict) -> float:
    TB = target_balance(name, tokens)
    return redeemed * TB / tokens[name].supply


def get_price_impact_loss(a_in: float, t_in: Token, t_out: Token):
    a_out = amount_out(a_in, t_in, t_out)
    # price_impact_loss = (1 - SWAP_FEE) * (a_out - a_in *
    #                                       (t_in.price / t_out.price)) * t_out.price
    price_impact_loss = (a_out - a_in *
                         (t_in.price / t_out.price)) * t_out.price
    return price_impact_loss
