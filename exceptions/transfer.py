class NotEnoughBalanceException(Exception):
    def __init__(self, message="Not enough balance to make transfer"):
        super().__init__(message)
