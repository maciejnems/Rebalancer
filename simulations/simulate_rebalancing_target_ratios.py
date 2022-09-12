from cadCAD.configuration.utils import config_sim
from rebalancer import state_updates, policies,  utils, genesis
from rebalancer.names import POOL, BLOCK, PROFIT, POPULARITY, TRADING_VOLUME, MAX_HISTORY


def aggregator(a, b):
    return a+b


def append(experiment, blocks):
    historical_data = utils.get_historical_data()
    user_record, genesis_state = genesis.get_state_from_historical_data(
     historical_data)

    sim_config = config_sim(
        {
            "N": 1,
            "T": range(blocks),
        }
    )

    psubs = [
        {
            "policies": {
                'user_policy': policies.get_user_policy()
            },
            "variables": {
                PROFIT: state_updates.profit_update,
                POOL: state_updates.get_pool_state_upadate(user_record, historical_data, True),
                BLOCK: state_updates.block_update,
                POPULARITY: state_updates.get_popularity_update(historical_data),
                TRADING_VOLUME: state_updates.trading_volume_update,
                MAX_HISTORY: state_updates.prune_state_history,
            }
        },
    ]

    experiment.append_model(
        model_id='rebalancing_target_ratios',
        sim_configs=sim_config,
        initial_state=genesis_state,
        partial_state_update_blocks=psubs,
        policy_ops=[aggregator]
    )
