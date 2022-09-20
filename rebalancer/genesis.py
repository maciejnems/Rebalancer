from rebalancer.model import Time, Token, VALUE_PER_TOKEN, TX_PER_DAY
from rebalancer.policies import SWAP_MEAN
from rebalancer.names import TIMESTAMP, POOL, PROFIT, ARBITRAGEUR_PROFIT, NORMAL_PROFIT, POPULARITY, TRADING_VOLUME, MAX_HISTORY
from rebalancer import formulas


def get_state_from_historical_data(historical_data, tx_per_day):
    # value_sum = sum([d.iloc[0].market_cap for d in historical_data.values()])
    # tokens = {t: Token(t, VALUE_PER_TOKEN / d.iloc[0].price,
    #                    d.iloc[0].market_cap / value_sum, d.iloc[0].price) for t, d in historical_data.items()}
    tokens = {t: Token(t, VALUE_PER_TOKEN / d.iloc[0].price,
                       1/len(historical_data), d.iloc[0].price) for t, d in historical_data.items()}
    target_balances = formulas.target_balances(tokens)
    for t, tr in target_balances.items():
        tokens[t].balance = tr
        tokens[t].supply = tr

    popularity_sum = sum(
        [ph.iloc[0].total_volume for ph in historical_data.values()])
    popularity = {t: d.iloc[0].total_volume /
                  popularity_sum for t, d in historical_data.items()}

    user_record = {
        "root": {
            name: t.supply for name, t in tokens.items()
        }
    }

    genesis_state = {
        TIMESTAMP: Time(0, 0, tx_per_day[0]),
        POOL: tokens,
        PROFIT: {
            ARBITRAGEUR_PROFIT: [0, 0, 0],
            NORMAL_PROFIT: [0, 0, 0],
        },
        MAX_HISTORY: 10,
        POPULARITY: popularity,
        TRADING_VOLUME: {name: {} for name in tokens.keys()}
    }

    return user_record, genesis_state
