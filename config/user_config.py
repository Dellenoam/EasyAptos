# Transaction Settings
gas_unit_price = 100  # price per gas unit
max_gas_amount = 1000  # max gas amount per transaction you ready to pay
delay_between_transactions = [2, 4]  # delay between transactions (in seconds)
wait_for_transaction = True  # wait for transaction completion
transaction_wait_in_seconds = 60  # wait time for transaction completion (in seconds)
retries = 3  # number of retries on transaction failure

# Transfer Settings
use_all_balance = False  # transfer all balance
transfer_amount = [1, 2]  # transfer amount in APT. if use_all_balance is True, then this value will be ignored

# Async Settings
use_concurrency = True  # use concurrency (async)
concurrency_limit = 10  # concurrency limit

# General Settings
play_intro = False  # play intro on start of the script
debug_mode = True  # use testnet or mainnet
