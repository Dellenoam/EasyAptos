from typing import List, Tuple

from aptos_sdk.account import Account

from config.app_config import app_settings
from utils.spreadsheet_utils import write_create_wallets_to_xlsx


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


def create_wallets() -> None:
    while True:
        try:
            number_of_wallets = int(
                input("Enter the number of wallets to create or 0 to cancel: ")
            )
            if number_of_wallets <= 0:
                print("\nInvalid number. Please enter a positive integer.\n")
                continue
            break
        except ValueError:
            print("\nInvalid input. Please enter an integer.\n")

    wallet_creator_service = WalletCreatorService()
    try:
        created_wallets = wallet_creator_service.perform_wallet_creation(
            number_of_wallets
        )
        write_create_wallets_to_xlsx(
            created_wallets, app_settings.output.WALLET_CREATION_RESULT_PATH
        )
        print(
            f"\nWallets created and saved to {app_settings.output.WALLET_CREATION_RESULT_PATH}"
        )
    except Exception as error:
        print(f"\nError creating wallets | Error: {error}")
