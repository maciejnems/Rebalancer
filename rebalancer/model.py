class Token:
    def __init__(self, name: str, balance: float, tr: float, price: float):
        self.name = name
        self.balance = balance
        self.target_ratio = tr
        self.price = price
        self.supply = balance

    def __repr__(self):
        repr = {"name": self.name, "balance": self.balance,
                "target_ratio": self.target_ratio, "price": self.price, "supply": self.supply}
        return f'{self.name}: B: {self.balance} TR: {self.target_ratio} P: {self.price} S: {self.supply}'


class Time:
    def __init__(self, day, block, block_limit):
        self.day = day
        self.block = block
        self.block_limit = block_limit

    def __repr__(self):
        repr = {"day": self.day, "block": self.block,
                "block_limit": self.block_limit}
        return f'{repr}'
