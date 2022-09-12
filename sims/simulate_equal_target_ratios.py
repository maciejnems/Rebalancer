from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import config_sim
from rebalancer import state_updates, policies,  utils, genesis
from rebalancer.names import POOL, TIME, PROFIT, POPULARITY, TRADING_VOLUME, MAX_HISTORY
# from sims.parameters import SIMULATION_LENGTH


def aggregator(a, b):
    return a+b


def append(experiment, blocks):
    historical_data = utils.get_historical_data()
    blocks, trading_volumes, user_record, genesis_state = genesis.get_state_from_historical_data(
        blocks, historical_data, False)

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
                POOL: state_updates.get_pool_state_upadate(user_record, historical_data),
                TIME: state_updates.get_time_update(trading_volumes),
                POPULARITY: state_updates.get_popularity_update(historical_data),
                TRADING_VOLUME: state_updates.trading_volume_update,
                MAX_HISTORY: state_updates.prune_state_history,
            }
        },
    ]

    experiment.append_model(
        model_id='equal_target_ratios',
        sim_configs=sim_config,
        initial_state=genesis_state,
        partial_state_update_blocks=psubs,
        policy_ops=[aggregator]
    )
