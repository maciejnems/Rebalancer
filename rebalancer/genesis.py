from rebalancer.model import Token
from rebalancer.names import BLOCK, POOL, PROFIT, ARBITRAGEUR_PROFIT, NORMAL_PROFIT, POPULARITY, TRADING_VOLUME
from rebalancer import formulas


def get_state(tokens, balances, target_ratios, prices):
    return {
        BLOCK: 0,
        POOL: {t: Token(t, b, tr, p) for t, b, tr, p in zip(
            tokens, balances, target_ratios, prices)},
        PROFIT: {
            ARBITRAGEUR_PROFIT: 0,
            NORMAL_PROFIT: 0,
        },
    }


def get_state_from_historical_data(historical_data):
    value_sum = sum([d.iloc[0].market_cap for d in historical_data.values()])
    tokens = {t: Token(t, d.iloc[0].market_cap / (100000 * d.iloc[0].price),
                       d.iloc[0].market_cap / value_sum, d.iloc[0].price) for t, d in historical_data.items()}
    # tokens = {t: Token(t, d.iloc[0].market_cap / (100000 * d.iloc[0].price),
    #                    1 / len(historical_data), d.iloc[0].price) for t, d in historical_data.items()}
    target_balances = formulas.target_balances(tokens)
    for t, tr in target_balances.items():
        tokens[t].balance = tr

    popularity_sum = sum(
        [ph.iloc[0].total_volume for ph in historical_data.values()])
    return {
        BLOCK: 0,
        POOL: tokens,
        PROFIT: {
            ARBITRAGEUR_PROFIT: 0,
            NORMAL_PROFIT: 0,
        },
        POPULARITY: {
            t: d.iloc[0].total_volume / popularity_sum for t, d in historical_data.items()
        },
        TRADING_VOLUME: {}
    }
