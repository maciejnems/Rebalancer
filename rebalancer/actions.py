import imp
from rebalancer.formulas import amount_out
from rebalancer.model import Token


def swap(a_in: float, t_in: Token, t_out: Token):
    a_out = amount_out(a_in, t_in, t_out)
    t_in.balance += a_in
    t_out.balance -= a_out
    return t_in, t_out, a_out
