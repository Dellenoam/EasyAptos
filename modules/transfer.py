from random import randint
from typing import Dict

from aptos_sdk.account import Account
from aptos_sdk.account_address import AccountAddress
from aptos_sdk.async_client import RestClient

from config.app_config import app_settings
from config.user_config import (
    debug_mode,
    gas_unit_price,
    max_gas_amount,
    retries,
    transaction_wait_in_seconds,
    transfer_amount,
    use_all_balance,
    wait_for_transaction,
)


class TransferService:
    def __init__(self, private_key, destination_address):
        self._account = Account.load_key(private_key)
        self.destination_address: str = destination_address
        if debug_mode:
            self._client = RestClient(app_settings.aptos.APTOS_NODE_TESTNET_URL)
        else:
            self._client = RestClient(app_settings.aptos.APTOS_NODE_MAINNET_URL)

    async def perform_transfer(self) -> Dict[str, str | int]:
        sender_balance = await self._client.account_balance(self._account.address())
        estimated_gas_cost = gas_unit_price * max_gas_amount
        transfer_amount = self._calculate_transfer_amount(
            sender_balance, estimated_gas_cost
        )
        transaction_data = await self._send_transaction(transfer_amount)

        return transaction_data

    def _calculate_transfer_amount(
        self, sender_balance: int, estimated_gas_cost: int
    ) -> int:
        if use_all_balance:
            if sender_balance < estimated_gas_cost:
                print(sender_balance, estimated_gas_cost)
                raise Exception("Not enough balance to cover gas cost")
            return sender_balance - estimated_gas_cost
        else:
            if sender_balance < transfer_amount[1] * int(1e8) + estimated_gas_cost:
                print(sender_balance, estimated_gas_cost)
                raise Exception("Not enough balance to cover gas cost")

            return randint(
                transfer_amount[0] * int(1e8),
                transfer_amount[1] * int(1e8),
            )

    async def _send_transaction(self, transfer_amount: int) -> Dict[str, str | int]:
        self._client.client_config.gas_unit_price = gas_unit_price
        self._client.client_config.max_gas_amount = max_gas_amount
        self._client.client_config.transaction_wait_in_seconds = (
            transaction_wait_in_seconds
        )

        txn_hash = None
        for _ in range(retries):
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

                if not wait_for_transaction:
                    break

                print("Waiting for transaction to complete...")

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
