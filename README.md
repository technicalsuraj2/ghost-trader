# Ghost Trader - MT5 Auto Trade

A Kali Linux-friendly launcher + desktop controller for MetaTrader 5 auto trading.

- **`ghost_trader.py`** - animated **GHOST TRADE** banner (saffron/kesari colour) with intro
  animation, then a menu:
  1. **Start Auto Trade** - opens the MT5 controller in a new window/tab
  2. **Go to Author Account** - redirects to the author's GitHub
  3. **Exit**
- **`mt5_control_app.py`** - the MT5 desktop controller (BUY/SELL/close-all, profit
  target / max-loss auto close). Credentials remain session-only.

## Install on Kali Linux

Requirements: Linux desktop (X/Wayland), Python 3.10+, and the MetaTrader 5 terminal.
The official `MetaTrader5` pip wheel is **Windows-only**, so on Kali run the MT5
terminal under **Wine** and install the module inside a Windows/Wine Python, or keep
the controller for testing which runs as a new window from the launcher.

```bash
git clone https://github.com/technicalsuraj2/ghost-trader.git
cd ghost-trader
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
ghost-trader
```

No dependencies are required to run the launcher banner + menu. To run the MT5
controller you additionally need `MetaTrader5` (see above).

## Using it safely

1. Open MT5 and log into the correct broker account.
2. In Market Watch, confirm the broker's exact symbol name - e.g. `EURUSD`, `EURUSDm`, or `BTCUSD`.
3. In the tool, click **Use active MT5 session**, then **Preflight**.
4. Begin with a demo account and a small lot. Turn on **Execute orders** only when the displayed account and symbol are correct.

This is a local controller, not investment advice. Trading can lose money; no profit is guaranteed.

## License

MIT