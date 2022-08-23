from cadCAD.configuration.utils import config_sim
from cadCAD.configuration import Experiment
from rebalancer.model import Token
from rebalancer import state_updates, policies

# Genesis States
genesis_states = {
    'USDC': Token('USDC', 1000.0, 0.5, 1.0),
    'USDT': Token('USDT', 890.0, 0.5, 1.0)
}


psubs = [
    {
        "policies": {
            'user_action': policies.user_action
        },
        "variables": {
            n: state_updates.get_token_policy(n) for n in genesis_states.keys()
        }
    }
]


sim_config = config_sim(
    {
        "N": 1,
        "T": range(10),
    }
)


def aggregator(a, b):
    return a+b


exp = Experiment()
exp.append_model(
    model_id='sys_model_A',
    sim_configs=sim_config,
    initial_state=genesis_states,
    partial_state_update_blocks=psubs,
    policy_ops=[aggregator]
)
