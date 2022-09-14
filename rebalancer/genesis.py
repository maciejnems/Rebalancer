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

    trading_volume = {name: {} for name in tokens.keys()}
    for t_in, volume in trading_volume.items():
        for t_out in trading_volume.keys():
            if t_out != t_in:
                volume[t_out] = popularity[t_in] * \
                    popularity[t_out] * TX_PER_DAY * SWAP_MEAN

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
        TRADING_VOLUME: trading_volume
    }

    return user_record, genesis_state
