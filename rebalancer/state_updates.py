def get_token_policy(name: str):

    def token_policy(_g, step, sH, s, input):
        if name in input:
            return (name, input[name])
        else:
            return (name, s[name])

    return token_policy
