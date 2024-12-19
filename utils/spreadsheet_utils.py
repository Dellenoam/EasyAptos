import csv
import os
from typing import Dict, List, Tuple

from openpyxl import Workbook

from config.user_config import debug_mode


def read_wallets_from_csv(filename: str) -> List[Tuple[str, str, str]] | None:
    wallets = []

    if not os.path.exists(filename):
        return None

    with open(filename, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            name, private_key, destination_address = row

            if not name:
                name = str(len(wallets) + 1)

            if not private_key.startswith("ed25519-priv-"):
                private_key = "ed25519-priv-" + private_key

            wallets.append((name, private_key, destination_address))

    return wallets


def write_balances_to_xlsx(
    filename: str,
    wallet_name: str,
    all_wallets_data: List[Tuple[str, Dict[str, Dict[str, int]]]],
) -> None:
    workbook = Workbook()

    default_sheet = workbook.active
    if default_sheet is not None:
        workbook.remove(default_sheet)

    sheet = workbook.create_sheet(title="Balances")

    sheet.append(["Wallet Name", "Wallet Address", "APT"])

    for wallet_name, wallet_data in all_wallets_data:
        for wallet_address, balances in wallet_data.items():
            apt_balance = balances.get("APT", 0.0)
            row = [wallet_name, wallet_address, apt_balance]
            sheet.append(row)

    for column_cells in sheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = length + 2

    workbook.save(filename)


def write_transactions_to_xlsx(
    filename, all_transaction_data: List[Tuple[str, str, int]]
) -> None:
    workbook = Workbook()

    default_sheet = workbook.active
    if default_sheet is not None:
        workbook.remove(default_sheet)

    sheet = workbook.create_sheet(title="Transactions")

    sheet.append(["Wallet Name", "Transaction Link", "Transfered Amount (APT)"])

    for wallet_name, txn_hash, transfered_amount in all_transaction_data:
        aptos_explorer_transaction_url = "https://explorer.aptoslabs.com/txn/"
        aptos_explorer_transaction_url += txn_hash
        if debug_mode:
            aptos_explorer_transaction_url += "?network=testnet"
        else:
            aptos_explorer_transaction_url += "?network=mainnet"

        sheet.append([wallet_name, aptos_explorer_transaction_url, transfered_amount])

        for column_cells in sheet.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            sheet.column_dimensions[column_cells[0].column_letter].width = length + 2

        workbook.save(filename)


def write_create_wallets_to_xlsx(wallets: List[Tuple[str, str]], filename: str) -> None:
    workbook = Workbook()

    default_sheet = workbook.active
    if default_sheet is not None:
        workbook.remove(default_sheet)

    sheet = workbook.create_sheet(title="Wallets")

    sheet.append(["Name", "Wallet Address", "Wallet Private Key"])
    for index, (private_key, destination_address) in enumerate(wallets, start=1):
        name = str(index)
        sheet.append([name, private_key, destination_address])

    for column_cells in sheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells)
        sheet.column_dimensions[column_cells[0].column_letter].width = length + 2

    workbook.save(filename)
