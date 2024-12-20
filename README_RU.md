🇺🇸 [English README](https://github.com/Dellenoam/EasyAptos/blob/master/README.md)

# EasyAptos 🐸

Скрипт для различных задач в сети Aptos

## Требования

[![Python](https://img.shields.io/badge/python-%3E%3D3.10-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://www.python.org/)

## Возможности

<table>
  <thead>
    <tr>
      <th>Функция</th>
      <th>Поддержка</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Супер-Мега-Крутое интро с капибарой</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Проверка баланса</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Перевод APT с одного кошелька на другой</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>Генератор кошельков</td>
      <td>✅</td>
    </tr>
  </tbody>
</table>

## Настройки

<table>
  <thead>
    <tr>
      <th>Опция</th>
      <th>Описание</th>
    </tr>
  </thead>
  <tbody>
    <!-- Настройки транзакции -->
    <tr>
      <td>gas_unit_price</td>
      <td>Цена за единицу газа для транзакции</td>
    </tr>
    <tr>
      <td>max_gas_amount</td>
      <td>Максимальное количество газа, которое вы готовы заплатить за транзакцию</td>
    </tr>
    <tr>
      <td>delay_between_transactions</td>
      <td>Диапазон задержки (в секундах) между транзакциями</td>
    </tr>
    <tr>
      <td>wait_for_transaction</td>
      <td>True/False указывает, должен ли скрипт дождаться завершения транзакции, прежде чем продолжить</td>
    </tr>
    <tr>
      <td>transaction_wait_in_seconds</td>
      <td>Максимальное время ожидания (в секундах) завершения транзакции</td>
    </tr>
    <tr>
      <td>retries</td>
      <td>Допустимое количество повторных попыток в случае сбоя транзакции</td>
    </tr>
    <!-- Настройки перевода -->
    <tr>
      <td>use_all_balance</td>
      <td>Значение True/False указывает, следует ли переводить все доступные средства</td>
    </tr>
    <tr>
      <td>transfer_amount</td>
      <td>Диапазон сумм перевода (APT). Если use_all_balance равно True, то сумма перевода будет равна всем доступным средствам</td>
    </tr>
    <!-- Общие настройки -->
    <tr>
      <td>play_intro</td>
      <td>True/False для воспроизведения интро при запуске скрипта.</td>
    </tr>
    <tr>
      <td>debug_mode</td>
      <td>True/False для переключения между тестовой сетью (режим отладки) и основной сетью.</td>
    </tr>
  </tbody>
</table>

## Как установить 📚

Прежде чем начать, убедитесь, что соблюдены все [требованиям](#requirements). Это ВАЖНО, без этого вы не сможете установить наш скрипт.

### Установка Linux вручную

```shell
git clone https://github.com/Dellenoam/EasyAptos.git
cd EasyAptos
python3 -m venv .venv
source .venv/bin/активировать
установку pip poetry
poetry install -только главная
```

### Ручная установка Windows

```shell
git clone https://github.com/Dellenoam/EasyAptos.git
cd EasyAptos
python -m venv .venv
.venv\Scripts\activate
pip установить poetry
poetry install -только главная
```

### Конфигурация

Вы можете настроить скрипт, отредактировав файл `config/user_config.py`. Чтобы узнать больше о параметрах, ознакомьтесь с разделом [настройки](#settings).

## Как импортировать кошельки

Чтобы импортировать кошельки в скрипт, вам нужно вставить приватные ключи в private_keys.txt и адрес получателей в recipients.txt. При этом количество приватных ключей должно совпадать с количеством адресов получателей.

## Запустите скрипт

![EasyAptos Intro](https://github.com/Dellenoam/EasyAptos/blob/master/assets/EasyAptos_Intro.gif)

### Использование start.bat

Вы можете запустить скрипт с помощью скрипта start.bat, просто запустите его.

### Вручную

Перед запуском скрипта вам всегда нужно активировать виртуальную среду и проверить наличие обновлений.

```shell
# Linux
source .venv\bin\activate
# Windows
.venv\Scripts\activate

# Linux/Windows
git pull
```

Чтобы запустить скрипт, используйте `python3 main.py` на Linux или `python main.py` на Windows.

## Контакты

Если у вас есть какие-либо вопросы или предложения, не стесняйтесь обращаться к нам в комментарии.

[![Capybara Society Telegram Channel](https://img.shields.io/badge/Capybara%20Society-Join-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/capybara_society)