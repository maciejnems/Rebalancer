from cadCAD.configuration.utils import config_sim
from rebalancer import state_updates, policies,  utils, genesis
from rebalancer.names import POOL, TIMESTAMP, PROFIT, POPULARITY, MAX_HISTORY, POPULARIT_CACHE, UPDATE_INTERVAL


def aggregator(a, b):
    return a+b


def append(experiment, blocks, historical_data, tx_per_day):
    user_record, genesis_state = genesis.get_state_from_historical_data(
        historical_data, tx_per_day)

    sim_config = config_sim(
        {
            "N": 1,
            "T": range(blocks),
            "M": {POPULARIT_CACHE: [None], UPDATE_INTERVAL: [1]},
        }
    )

    psubs = [
        {
            "policies": {
                'user_policy': policies.get_user_policy()
            },
            "variables": {
                PROFIT: state_updates.profit_update,
                POOL: state_updates.get_pool_state_upadate(user_record, historical_data, False),
                TIMESTAMP: state_updates.get_timestamp_update(tx_per_day),
                POPULARITY: state_updates.get_popularity_update(historical_data),
                MAX_HISTORY: state_updates.prune_state_history,
            }
        },
    ]

    experiment.append_model(
        model_id='Balancer',
        sim_configs=sim_config,
        initial_state=genesis_state,
        partial_state_update_blocks=psubs,
        policy_ops=[aggregator]
    )
