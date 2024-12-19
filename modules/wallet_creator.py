from typing import List, Tuple

from aptos_sdk.account import Account


class WalletCreatorService:
    def perform_wallet_creation(self, count: int) -> List[Tuple[str, str]]:
        return self._create_wallets(count)

    def _create_wallets(self, count: int) -> List[Tuple[str, str]]:
        created_wallets = []

        for _ in range(count):
            account = Account.generate()

            wallet_address = account.address().__repr__()
            wallet_private_key = account.private_key.hex()

            created_wallets.append((wallet_address, wallet_private_key))

        return created_wallets
