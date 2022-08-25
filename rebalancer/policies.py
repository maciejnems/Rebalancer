from rebalancer.names import ACTION_PROVIDE_LIQUIDITY, ACTION_REMOVE_LIQUIDITY, ACTION_SWAP, ACTION, ARGUMENTS, BLOCK


def get_user_policy(dictionary):
    dictionary["user"] = {"USDC": 1}

    def user_policy(_g, step, sH, s):
        print("user_policy", dictionary)
        dictionary["user"]["USDC"] += 1
        return {}
    return user_policy


def user_policy(_g, step, sH, s):
    print("Step: ", s[BLOCK])
    if s[BLOCK] == 0:
        return {ACTION: ACTION_PROVIDE_LIQUIDITY, ARGUMENTS: [50.0, "USDC", "some user"]}
    elif s[BLOCK] <= 4:
        return {ACTION: ACTION_REMOVE_LIQUIDITY, ARGUMENTS: [10.0, "USDC", "some user"]}
    elif s[BLOCK] == 5:
        return {ACTION: ACTION_REMOVE_LIQUIDITY, ARGUMENTS: [None, "USDC", "some user"]}
    return {ACTION: None}
