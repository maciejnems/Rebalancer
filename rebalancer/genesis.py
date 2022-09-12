from rebalancer.model import Time, Token
from rebalancer.state_updates import TX_PER_DAY
from rebalancer.policies import SWAP_MEAN
from rebalancer.names import POOL, PROFIT, ARBITRAGEUR_PROFIT, NORMAL_PROFIT, POPULARITY, TRADING_VOLUME, MAX_HISTORY, REBALANCE, TIME
from rebalancer import formulas
import pandas as pd


def get_state(tokens, balances, target_ratios, prices):
    return {

        POOL: {t: Token(t, b, tr, p) for t, b, tr, p in zip(
            tokens, balances, target_ratios, prices)},
        PROFIT: {
            ARBITRAGEUR_PROFIT: 0,
            NORMAL_PROFIT: 0,
        },
    }


BALANCE = 1_000_000


def get_state_from_historical_data(blocks, historical_data, should_rebalance):
    # value_sum = sum([d.iloc[0].market_cap for d in historical_data.values()])
    # tokens = {t: Token(t, BALANCE / d.iloc[0].price,
    #                    d.iloc[0].market_cap / value_sum, d.iloc[0].price) for t, d in historical_data.items()}
    tokens = {t: Token(t, BALANCE / d.iloc[0].price,
                       1/len(historical_data), d.iloc[0].price) for t, d in historical_data.items()}
    target_balances = formulas.target_balances(tokens)
    for t, tr in target_balances.items():
        tokens[t].balance = tr
        tokens[t].supply = tr

    popularity_sum = sum(
        [ph.iloc[0].total_volume for ph in historical_data.values()])
    popularity = {t: d.iloc[0].total_volume /
                  popularity_sum for t, d in historical_data.items()}

    trading_volume = {name: {} for name in tokens.keys()}
    for t_in, volume in trading_volume.items():
        for t_out in trading_volume.keys():
            if t_out != t_in:
                volume[t_out] = popularity[t_in] * \
                    popularity[t_out] * TX_PER_DAY * SWAP_MEAN

    trading_volumes = pd.DataFrame.sum(pd.DataFrame(
        [hd["total_volume"] for hd in historical_data.values()]))
    whole_volume = pd.DataFrame.sum(trading_volumes.iloc[:-1])
    divisior = whole_volume / blocks
    trading_volumes = (trading_volumes / divisior).round()
    # print(trading_volumes)
    # print(whole_volume / 60000)
    print(min(trading_volumes), max(trading_volumes))
    user_record = {
        "root": {
            name: t.supply for name, t in tokens.items()
        }
    }

    # print(should_rebalance, formulas.compute_V(tokens))
    genesis_state = {
        TIME: Time(0, 0, trading_volumes.iloc[0]),
        REBALANCE: should_rebalance,
        POOL: tokens,
        PROFIT: {
            ARBITRAGEUR_PROFIT: [0, 0, 0],
            NORMAL_PROFIT: [0, 0, 0],
        },
        MAX_HISTORY: 2000,
        POPULARITY: popularity,
        TRADING_VOLUME: trading_volume
    }

    return int(sum(trading_volumes.iloc[:-1])), trading_volumes, user_record, genesis_state
