🇷🇺 [Russian README](https://github.com/Dellenoam/EasyAptos/blob/master/README_RU.md)

# EasyAptos 🐸

Script for various tasks in the Aptos network

## Requirements

[![Python](https://img.shields.io/badge/python-%3E%3D3.10-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://www.python.org/)

## Features  

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Supported</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>SuperMegaCool Capybara intro</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Balance checker</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Transfer APT from one wallet to another</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Wallet generator</td>
      <td>✅</td>
    </tr>
  </tbody>
</table>

## Settings

<table>
  <thead>
    <tr>
      <th>Option</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <!-- Transaction Settings -->
    <tr>
      <td>gas_unit_price</td>
      <td>Price per gas unit for the transaction</td>
    </tr>
    <tr>
      <td>max_gas_amount</td>
      <td>Maximum gas amount you are ready to pay per transaction</td>
    </tr>
    <tr>
      <td>delay_between_transactions</td>
      <td>Delay range (in seconds) between transactions</td>
    </tr>
    <tr>
      <td>wait_for_transaction</td>
      <td>True/False indicating if the script should wait for the transaction to complete before proceeding</td>
    </tr>
    <tr>
      <td>transaction_wait_in_seconds</td>
      <td>Maximum wait time (in seconds) for a transaction to complete</td>
    </tr>
    <tr>
      <td>retries</td>
      <td>Number of retries allowed if a transaction fails</td>
    </tr>
    <!-- Transfer Settings -->
    <tr>
      <td>use_all_balance</td>
      <td>True/False to indicate whether to transfer the entire balance</td>
    </tr>
    <tr>
      <td>transfer_amount</td>
      <td>Transfer amount range (APT). If use_all_balance is True, the transfer amount will be the entire balance</td>
    </tr>
    <!-- General Settings -->
    <tr>
      <td>play_intro</td>
      <td>True/False to play intro on script start.</td>
    </tr>
    <tr>
      <td>debug_mode</td>
      <td>True/False to toggle between testnet (debug mode) and mainnet.</td>
    </tr>
  </tbody>
</table>

## How to install 📚

Before you begin, make sure you have meet the [requirements](#requirements). It's really IMPORTANT, without these requiremenets, you can NOT install our script.

### Linux manual installation

```shell
git clone https://github.com/Dellenoam/EasyAptos.git
cd EasyAptos
python3 -m venv .venv
source .venv/bin/activate
pip install poetry
poetry install --only main
```

### Windows manual installation

```shell
git clone https://github.com/Dellenoam/EasyAptos.git
cd EasyAptos
python -m venv .venv
.venv\Scripts\activate
pip install poetry
poetry install --only main
```

### Configuration

You can configure the script by editing the `config/user_config.py` file. To learn more about options, see the [settings](#settings).

### How to import wallets

To import wallets into the script, create a table wallets.csv in the root directory of the script. For an example, see [wallets_template.csv](https://github.com/Dellenoam/EasyAptos/blob/master/wallets_template.csv).

## Run the script

![EasyAptos Intro](https://github.com/Dellenoam/EasyAptos/blob/master/assets/EasyAptos_Intro.gif)

### Using start.bat

You can run the script using start.bat script, just execute it.

### Manually

Before running the script, you ALWAYS need to activate the virtual environment and check for updates.

```shell
# Linux
source .venv\bin\activate
# Windows
.venv\Scripts\activate

# Linux/Windows
git pull
```

To run the script, use `python3 main.py` on Linux or `python main.py` on Windows.

## Contacts

If you have any questions or suggestions, please feel free to contact us in comments.

[![Capybara Society Telegram Channel](https://img.shields.io/badge/Capybara%20Society-Join-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/capybara_society)