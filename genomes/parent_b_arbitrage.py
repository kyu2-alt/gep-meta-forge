import json

class FlashLoanArb:
    def __init__(self):
        self.flash_loan_fee = 0.0009

    def calculate_spread(self, reserve_a, reserve_b):
        spread = (reserve_a / reserve_b) - 1.0
        return spread

    def trigger_flashloan(self, amount):
        profit = amount * 0.02
        net_profit = profit - (amount * self.flash_loan_fee)
        return net_profit
