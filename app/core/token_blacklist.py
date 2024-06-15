from typing import Set

class TokenBlacklist:
    def __init__(self):
        self.blacklist: Set[str] = set()

    def add_token(self, token: str):
        self.blacklist.add(token)

    def is_blacklisted(self, token: str) -> bool:
        return token in self.blacklist

token_blacklist = TokenBlacklist()
