import asyncio
from random import randint, uniform
from typing import Dict, List, Tuple, cast

from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.async_client import RestClient

from config import user_config
from config.app_config import app_settings
from exceptions.transfer import NotEnoughBalanceException
from utils.spreadsheet_utils import write_transactions_to_xlsx


class TransferService:
    def __init__(self, private_key: str, destination_address: str):
        self._account = Account.load_key(private_key)
        self._client = self._get_client()
        self.destination_address: str = destination_address

    def _get_client(self) -> RestClient:
        if user_config.debug_mode:
            return RestClient(app_settings.aptos.APTOS_NODE_TESTNET_URL)
        return RestClient(app_settings.aptos.APTOS_NODE_MAINNET_URL)

    async def __aenter__(self) -> "TransferService":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self._client.close()

    async def perform_transfer(self) -> Dict[str, str | int]:
        sender_balance = await self._client.account_balance(self._account.address())
        estimated_gas_cost = user_config.gas_unit_price * user_config.max_gas_amount
        transfer_amount = self._calculate_transfer_amount(
            sender_balance, estimated_gas_cost
        )
        transaction_data = await self._send_transaction(transfer_amount)

        return transaction_data

    def _calculate_transfer_amount(
        self, sender_balance: int, estimated_gas_cost: int
    ) -> int:
        if user_config.use_all_balance:
            if sender_balance < estimated_gas_cost:
                raise NotEnoughBalanceException("Not enough balance to cover gas cost")
            return sender_balance - estimated_gas_cost
        else:
            if (
                sender_balance
                < user_config.transfer_amount[1] * int(1e8) + estimated_gas_cost
            ):
                raise NotEnoughBalanceException("Not enough balance to cover gas cost")

            return randint(
                user_config.transfer_amount[0] * int(1e8),
                user_config.transfer_amount[1] * int(1e8),
            )

    async def _send_transaction(self, transfer_amount: int) -> Dict[str, str | int]:
        self._client.client_config.gas_unit_price = user_config.gas_unit_price
        self._client.client_config.max_gas_amount = user_config.max_gas_amount
        self._client.client_config.transaction_wait_in_seconds = (
            user_config.transaction_wait_in_seconds
        )

        txn_hash = None
        for _ in range(user_config.retries):
            try:
                print(
                    f"\nTransfering {transfer_amount / 1e8} APT from {self._account.address().__repr__()} to {self.destination_address}"
                )

                txn_hash = await self._client.transfer_coins(
                    sender=self._account,
                    recipient=AccountAddress.from_str(self.destination_address),
                    coin_type="0x1::aptos_coin::AptosCoin",
                    amount=transfer_amount,
                )

                if not user_config.wait_for_transaction:
                    break

                await self._client.wait_for_transaction(txn_hash)
            except AssertionError as error:
                if "transaction timed out" in str(error):
                    continue
                else:
                    raise Exception("Transaction failed")

            break
        else:
            raise Exception("Transaction timed out")

        transaction_data = {
            "txn_hash": txn_hash,
            "transfered_amount": transfer_amount / 1e8,
        }

        return transaction_data


async def start_transfer_process(wallets: List[Tuple[str, str, str]]) -> None:
    all_transaction_data = []

    semaphore = asyncio.Semaphore(user_config.concurrency_limit)

    async def transfer(wallet_data: Tuple[str, str, str]) -> None:
        wallet_name, private_key, destination_address = wallet_data
        try:
            if user_config.use_concurrency:
                async with semaphore:
                    async with TransferService(
                        private_key, destination_address
                    ) as transfer_service:
                        transaction_data = await transfer_service.perform_transfer()
            else:
                async with TransferService(
                    private_key, destination_address
                ) as transfer_service:
                    transaction_data = await transfer_service.perform_transfer()

            transaction_hash = cast(str, transaction_data.get("txn_hash", "N/A"))
            transfered_amount = cast(int, transaction_data.get("transfered_amount", 0))

            all_transaction_data.append(
                (wallet_name, transaction_hash, transfered_amount)
            )
        except NotEnoughBalanceException:
            print(f"\nNot enough balance to transfer from {wallet_name}. Skipping...")
            all_transaction_data.append((wallet_name, "N/A", "N/A"))
        except Exception as error:
            print(f"\nError transferring from {wallet_name} | Error: {error}")
            all_transaction_data.append((wallet_name, "N/A", "N/A"))

    if user_config.use_concurrency:
        chunk_size = user_config.concurrency_limit
        chunks = [
            wallets[i : i + chunk_size] for i in range(0, len(wallets), chunk_size)
        ]
        for chunk in chunks:
            await asyncio.gather(*(transfer(wallet_data) for wallet_data in chunk))
            if not chunk == chunks[-1]:
                min_delay, max_delay = user_config.delay_between_transactions
                random_sleep_time = uniform(min_delay, max_delay)
                print(f"\nSleeping for {random_sleep_time} seconds...")
                await asyncio.sleep(random_sleep_time)
    else:
        for wallet_data in wallets:
            await transfer(wallet_data)
            if not wallet_data == wallets[-1]:
                min_delay, max_delay = user_config.delay_between_transactions
                random_sleep_time = uniform(min_delay, max_delay)
                print(f"\nSleeping for {random_sleep_time} seconds...")
                await asyncio.sleep(random_sleep_time)

    write_transactions_to_xlsx(
        app_settings.output.TRANSACTIONS_RESULT_PATH, sorted(all_transaction_data)
    )

    print(
        f"\nTransfer process completed and saved to {app_settings.output.TRANSACTIONS_RESULT_PATH}"
    )
