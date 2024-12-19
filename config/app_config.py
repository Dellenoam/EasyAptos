from pydantic import BaseModel


class AptosConfig(BaseModel):
    APTOS_NODE_MAINNET_URL: str = "https://fullnode.mainnet.aptoslabs.com/v1"
    APTOS_NODE_TESTNET_URL: str = "https://fullnode.testnet.aptoslabs.com/v1"


class OutputConfig(BaseModel):
    BALANCES_RESULT_PATH: str = "output/balances.xlsx"
    TRANSACTIONS_RESULT_PATH: str = "output/transactions.xlsx"
    WALLET_CREATION_RESULT_PATH: str = "output/created_wallets.xlsx"


class AppSettings(BaseModel):
    aptos: AptosConfig = AptosConfig()
    output: OutputConfig = OutputConfig()


app_settings = AppSettings()
