from typing import Dict

from aptos_sdk.account import Account
from aptos_sdk.async_client import RestClient

from config.app_config import app_settings
from config.user_config import debug_mode


async def get_balances(private_key) -> Dict[str, Dict[str, int]]:
    account = Account.load_key(private_key)
    if debug_mode:
        client = RestClient(app_settings.aptos.APTOS_NODE_TESTNET_URL)
    else:
        client = RestClient(app_settings.aptos.APTOS_NODE_MAINNET_URL)

    wallet_address = account.address().__repr__()
    account_resources = await client.account_resources(account.address())

    wallet_data = {}

    for resource in account_resources:
        if resource["type"] == "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>":
            if int(resource["data"]["coin"]["value"]) / 1e8 == 0:
                continue
            wallet_data[wallet_address] = {
                "APT": int(resource["data"]["coin"]["value"]) / 1e8
            }
        elif resource["type"].startswith("0x1::coin::CoinStore<"):
            token_type = resource["type"].split("<")[1].split(">")[0]
            token_name = token_type.split("::")[-1]
            if int(resource["data"]["coin"]["value"]) / 1e8 == 0:
                continue
            wallet_data[wallet_address] = {
                token_name: int(resource["data"]["coin"]["value"]) / 1e8
            }

    return wallet_data
