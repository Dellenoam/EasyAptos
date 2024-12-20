import asyncio
from typing import Dict, List, Tuple

from aptos_sdk.account import Account
from aptos_sdk.async_client import AccountNotFound, RestClient

from config import user_config
from config.app_config import app_settings
from utils.spreadsheet_utils import write_balances_to_xlsx


class BalanceChecker:
    def __init__(self, private_key: str):
        self._account = Account.load_key(private_key)
        self._client = self._get_client()
        self.wallet_address = self._account.address().__repr__()

    def _get_client(self) -> RestClient:
        if user_config.debug_mode:
            return RestClient(app_settings.aptos.APTOS_NODE_TESTNET_URL)
        return RestClient(app_settings.aptos.APTOS_NODE_MAINNET_URL)

    async def __aenter__(self) -> "BalanceChecker":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._client.close()

    async def get_balances(self) -> Dict[str, Dict[str, int]]:
        account_resources = await self._client.account_resources(
            self._account.address()
        )

        wallet_data = {}

        for resource in account_resources:
            if resource["type"] == "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>":
                if int(resource["data"]["coin"]["value"]) / 1e8 == 0:
                    continue
                wallet_data[self.wallet_address] = {
                    "APT": int(resource["data"]["coin"]["value"]) / 1e8
                }
            elif resource["type"].startswith("0x1::coin::CoinStore<"):
                token_type = resource["type"].split("<")[1].split(">")[0]
                token_name = token_type.split("::")[-1]
                if int(resource["data"]["coin"]["value"]) / 1e8 == 0:
                    continue
                wallet_data[self.wallet_address] = {
                    token_name: int(resource["data"]["coin"]["value"]) / 1e8
                }

        return wallet_data


async def check_wallet_balances(wallets: List[Tuple[str, str, str]]) -> None:
    all_wallet_balances = []

    print("\nChecking wallet balances...")

    semaphore = asyncio.Semaphore(user_config.concurrency_limit)

    async def check_balance(wallet_data: Tuple[str, str, str]) -> None:
        wallet_name, private_key, _ = wallet_data
        try:
            if user_config.use_concurrency:
                async with semaphore:
                    async with BalanceChecker(private_key) as balance_checker:
                        wallet_balances = await balance_checker.get_balances()
            else:
                async with BalanceChecker(private_key) as balance_checker:
                    wallet_balances = await balance_checker.get_balances()

            all_wallet_balances.append((wallet_name, wallet_balances))
        except AccountNotFound:
            print(f"\nWallet {wallet_name} not found. Skipping...")
        except Exception as error:
            print(f"\nError checking balance for {wallet_name} | Error: {error}")
            all_wallet_balances.append((wallet_name, {}))

    if user_config.use_concurrency:
        await asyncio.gather(*(check_balance(wallet_data) for wallet_data in wallets))
    else:
        for wallet_data in wallets:
            await check_balance(wallet_data)

    if not all_wallet_balances:
        print("\nNo results to save")
        return

    write_balances_to_xlsx(
        app_settings.output.BALANCES_RESULT_PATH, "Wallets", sorted(all_wallet_balances)
    )

    print(f"\nBalances checked and saved to {app_settings.output.BALANCES_RESULT_PATH}")
