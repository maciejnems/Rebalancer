from rebalancer.model import Token
import math


def amount_out(a_in: float, t_in: Token, t_out: Token):
    return t_out.balance * \
        (1-(t_in.balance / math.exp(t_in.balance +
         a_in, t_in.target_ratio / t_out.target_ratio)))
