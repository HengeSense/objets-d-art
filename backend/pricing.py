class PricingBase:
    def __init__(self, amount, minus = 0):
        self.amount = amount
        self.minus = minus
        return (self.get_business_share(), self.get_client_share())

    def get_business_share(self): pass
    def get_client_share(self): pass

class DefaultPricing(PricingBase):
    def get_business_share(self):
        return self.amount * .5 - self.minus
    def get_client_share(self):
        return self.amount * .5
