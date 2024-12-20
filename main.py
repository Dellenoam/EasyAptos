import asyncio
import sys
from random import uniform
from typing import NoReturn, cast

from aptos_sdk.async_client import AccountNotFound

from config.app_config import app_settings
from config.user_config import delay_between_transactions, play_intro
from exceptions.transfer import NotEnoughBalanceException
from modules.balance_checker import get_balances
from modules.transfer import TransferService
from modules.wallet_creator import WalletCreatorService
from utils import banner_animation
from utils.spreadsheet_utils import (
    read_wallets_from_csv,
    write_balances_to_xlsx,
    write_create_wallets_to_xlsx,
    write_transactions_to_xlsx,
)


async def main() -> NoReturn:
    if play_intro:
        banner_animation.play_full_intro()
    else:
        banner_animation.print_script_text_art()

    wallets = read_wallets_from_csv("wallets.csv")
    if wallets is None:
        print(
            "\nNo wallets found in wallets.csv. Please add wallets or create new ones.\n"
        )

    print_options()
    choice = input("Enter your choice: ")

    if choice == "1":
        await check_wallet_balances(wallets)
    elif choice == "2":
        await start_transfer_process(wallets)
    elif choice == "3":
        await create_wallets()
    elif choice == "4":
        print("\nExiting the script.")
        sys.exit()
    else:
        print("\nInvalid choice. Please select 1, 2, 3, or 4.")


async def check_wallet_balances(wallets) -> None:
    if wallets is None:
        return

    all_wallets_data = []

    print("\nChecking wallet balances...")

    for wallet_data in wallets:
        wallet_name, private_key, _ = wallet_data
        try:
            wallet_data = await get_balances(private_key)
            all_wallets_data.append((wallet_name, wallet_data))
        except AccountNotFound:
            print(f"\nWallet {wallet_name} not found. Skipping...")
            continue
        except Exception as error:
            print(f"\nError checking balance for {wallet_name} | Error: {error}")
            user_input = input("Proceed to the next wallet? (Y/N): ")

            if user_input.lower() != "y":
                print("\nExiting the script.")
                sys.exit()

            continue

    if not all_wallets_data:
        print("\nNo results to save")
        return

    write_balances_to_xlsx(
        app_settings.output.BALANCES_RESULT_PATH, "Wallets", all_wallets_data
    )

    print(f"\nBalances checked and saved to {app_settings.output.BALANCES_RESULT_PATH}")


async def start_transfer_process(wallets) -> None:
    if wallets is None:
        return

    all_transaction_data = []

    for wallet_data in wallets:
        wallet_name, private_key, destination_address = wallet_data
        try:
            transfer_service = TransferService(private_key, destination_address)
            transaction_data = await transfer_service.perform_transfer()

            transaction_hash = cast(str, transaction_data.get("txn_hash", "N/A"))
            transfered_amount = cast(int, transaction_data.get("transfered_amount", 0))

            all_transaction_data.append(
                (wallet_name, transaction_hash, transfered_amount)
            )

            write_transactions_to_xlsx(
                app_settings.output.TRANSACTIONS_RESULT_PATH,
                all_transaction_data,
            )
        except NotEnoughBalanceException:
            print(f"\nNot enough balance to transfer from {wallet_name}. Skipping...")
            continue
        except Exception as error:
            print(f"\nError transferring from {wallet_name} | Error: {error}")

        if wallet_data is not wallets[-1]:
            min_delay = delay_between_transactions[0]
            max_delay = delay_between_transactions[1]
            random_sleep_time = uniform(min_delay, max_delay)
            print(f"\nSleeping for {random_sleep_time:.2f} seconds")
            await asyncio.sleep(random_sleep_time)

    print(
        f"\nTransfer process completed and saved to {app_settings.output.TRANSACTIONS_RESULT_PATH}"
    )


async def create_wallets() -> None:
    while True:
        try:
            number_of_wallets = int(input("Enter the number of wallets to create: "))
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


def print_options() -> None:
    print("""
1. Check wallet balances
2. Start transfer process
3. Create wallets
4. Exit
""")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
        sys.exit()
