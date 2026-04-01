import math
import time


class BillingEngine:
    def __init__(self, price_per_period=5.0, period_minutes=30):
        self.price_per_period = price_per_period
        self.period_sec = period_minutes * 60

    def calculate_fee(self, entry_time, current_time):
        duration_sec = current_time - entry_time

        periods = duration_sec / self.period_sec

        billed_periods = max(1, math.ceil(periods))

        return billed_periods * self.price_per_period
    
    def calculate_additional_fee(self, payment_time, current_time):
        duration_sec = current_time - payment_time

        periods = duration_sec / self.period_sec

        billed_periods = max(1, math.ceil(periods))

        return billed_periods * self.price_per_period
