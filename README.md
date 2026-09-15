# MT5 Auto Trader Controller

A Windows desktop tool for monitoring and managing positions in the **currently logged-in MetaTrader 5 desktop terminal**. It does not upload or store broker credentials.

## Features

- Connects to the active MT5 desktop terminal, so it works with an MT5 account from any supported broker.
- Checks an exact broker symbol through an order preflight before an order is submitted.
- Allows explicit BUY, SELL and Close all actions after the local **Execute orders** switch is enabled.
- Closes managed positions when their combined profit target or maximum-loss amount is reached.
- Keeps manual positions separate by default; enable the manual-position checkbox only when intended.

## Install and run

Requirements: Windows, Python 3.10+ and MetaTrader 5 desktop. Log into the desired demo account first.

```powershell
git clone https://github.com/YOUR-USERNAME/mt5-auto-trader-controller.git
cd mt5-auto-trader-controller
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install .
mt5-auto-trader
```

For local use without GitHub:

```powershell
cd C:\Users\admin\Documents\MT5-Auto-Trader
python -m pip install -r requirements.txt
python mt5_control_app.py
```

## Using it safely

1. Open MT5 and log into the correct broker account.
2. In Market Watch, confirm the broker's exact symbol name—for example `EURUSD`, `EURUSDm`, or `BTCUSD`.
3. In the tool, click **Use active MT5 session**, then **Preflight**.
4. Begin with a demo account and a small lot. Turn on **Execute orders** only when the displayed account and symbol are correct.

This is a local controller, not investment advice. Trading can lose money; no profit is guaranteed.
