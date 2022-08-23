class Token:
    def __init__(self, name: str, balance: float, tr: float, price: float):
        self.name = name
        self.balance = balance
        self.target_ratio = tr
        self.price = price

    def __repr__(self):
        return f'{self.name} balance: {self.balance} ratio: {self.target_ratio} price: {self.price}'
