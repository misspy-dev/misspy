class poll:
    def __init__(self, choices: list, multiple: bool=False, expiresAt: int=None, expiredAfter: int=None):
        self.choices = choices
        self.multiple = multiple
        self.expiresAt = expiresAt
        self.expiredAfter = expiredAfter