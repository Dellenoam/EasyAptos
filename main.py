import asyncio
import sys
from typing import NoReturn

from config.user_config import play_intro
from modules.balance_checker import check_wallet_balances
from modules.transfer import start_transfer_process
from modules.wallet_creator import create_wallets
from utils import banner_animation
from utils.spreadsheet_utils import read_wallets


async def main() -> NoReturn:
    if play_intro:
        banner_animation.play_full_intro()
    else:
        banner_animation.print_script_text_art()

    wallets = read_wallets()
    if not wallets:
        print(
            "\nNo wallets found. Please add them to the 'private_keys.txt' and 'recipients.txt' files.\n"
        )
        sys.exit()

    print_options()
    choice = input("Enter your choice: ")

    if choice == "1":
        await check_wallet_balances(wallets)
    elif choice == "2":
        await start_transfer_process(wallets)
    elif choice == "3":
        create_wallets()
    elif choice == "4":
        print("\nExiting the script.")
        sys.exit()
    else:
        print("\nInvalid choice. Please select 1, 2, 3, or 4.")


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
