from cadCAD.configuration.utils import config_sim
from rebalancer import state_updates, policies, genesis
from rebalancer.names import POOL, TIMESTAMP, USERS, POPULARITY, MAX_HISTORY


def aggregator(a, b):
    return a+b


def append(experiment, blocks, params, historical_data, tx_per_day, target_ratios=None):
    user_record, genesis_state = genesis.get_state_from_historical_data(
        historical_data, tx_per_day, target_ratios=target_ratios)

    sim_config = config_sim(
        {
            "N": 1,
            "T": range(blocks),
            "M": params,
        }
    )

    psubs = [
        {
            "policies": {
                'user_policy': policies.get_user_policy()
            },
            "variables": {
                USERS: state_updates.users_update,
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
