from cadCAD.configuration.utils import config_sim
from cadCAD.configuration import Experiment
from rebalancer.model import Token, get_genesis_state
from rebalancer import state_updates, policies, formulas
from rebalancer.names import POOL

tokens = ['USDC', 'USDT']

# Unbalanced Genesis State
genesis_states = get_genesis_state(
    tokens, [100000.0, 89000.0], [0.4, 0.6], [1.0, 1.0])

# Balanced Genesis State
# genesis_states = get_genesis_state(
#     tokens, [731.1041490513539, 1096.6562235770307], [0.4, 0.6], [1.0, 1.0])

user_record = {
    "root": {
        name: t.balance for name, t in genesis_states[POOL].items()
    }
}

psubs = [
    {
        "policies": {
            'user_policy': policies.get_user_policy()
        },
        "variables": {
            state_updates.get_pool_state_upadate(user_record),
            state_updates.block_update,
        }
    }
]


sim_config = config_sim(
    {
        "N": 1,
        "T": range(100),
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
