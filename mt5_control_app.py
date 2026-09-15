"""Compact MT5 desktop trading controller; credentials remain session-only."""
from __future__ import annotations

import threading
import time
import tkinter as tk
from dataclasses import dataclass
from tkinter import messagebox, scrolledtext, ttk

import MetaTrader5 as mt5


@dataclass
class Settings:
    symbol: str = "EURUSD"
    lot: float = 0.01
    profit_target: float = 0.30
    max_loss: float = 1.00
    poll_seconds: int = 5
    execute: bool = False
    manage_manual: bool = False


class App:
    def __init__(self, root: tk.Tk):
        self.root, self.connected, self.running = root, False, False
        self.stop_event = threading.Event()
        self.settings = Settings()
        root.title("MT5 Auto Trader")
        root.geometry("700x590")
        root.configure(bg="#151a22")
        s = ttk.Style(root); s.theme_use("clam")
        s.configure("TFrame", background="#151a22")
        s.configure("TLabel", background="#151a22", foreground="#e7edf5")
        s.configure("TCheckbutton", background="#151a22", foreground="#e7edf5")
        s.configure("TButton", background="#273142", foreground="#f4f7fb", padding=(7, 4))
        s.configure("TEntry", fieldbackground="#202936", foreground="#f3f6fb", insertcolor="#f3f6fb")
        form = ttk.Frame(root, padding=12); form.pack(fill="both", expand=True)
        form.columnconfigure(1, weight=1)
        self.symbol = self.field(form, "Symbol (exact MT5 name)", 0, "EURUSD")
        self.lot = self.field(form, "Lot per trade", 1, "0.01")
        self.profit = self.field(form, "Close profit target", 2, "0.30")
        self.loss = self.field(form, "Maximum loss", 3, "1.00")
        self.execute = tk.BooleanVar(value=False)
        self.manage_manual = tk.BooleanVar(value=False)
        self.minute_test = tk.BooleanVar(value=False)
        ttk.Checkbutton(form, text="Execute orders", variable=self.execute).grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 2))
        ttk.Checkbutton(form, text="Manage manual positions for this symbol", variable=self.manage_manual).grid(row=5, column=0, columnspan=2, sticky="w", pady=2)
        ttk.Checkbutton(form, text="Demo 1-minute test mode", variable=self.minute_test).grid(row=6, column=0, columnspan=2, sticky="w", pady=2)
        row = ttk.Frame(form); row.grid(row=7, column=0, columnspan=2, sticky="w", pady=8)
        ttk.Button(row, text="Use active MT5 session", command=self.connect).pack(side="left", padx=(0, 5))
        ttk.Button(row, text="Preflight", command=self.preflight).pack(side="left", padx=5)
        ttk.Button(row, text="BUY now", command=lambda: self.manual("BUY")).pack(side="left", padx=5)
        ttk.Button(row, text="SELL now", command=lambda: self.manual("SELL")).pack(side="left", padx=5)
        ttk.Button(row, text="Close all", command=self.close_all).pack(side="left", padx=5)
        ttk.Button(row, text="Start", command=self.start).pack(side="left", padx=5)
        ttk.Button(row, text="Stop", command=self.stop).pack(side="left", padx=5)
        self.status = tk.StringVar(value="Not connected")
        ttk.Label(form, textvariable=self.status).grid(row=8, column=0, columnspan=2, sticky="w", pady=4)
        self.log = scrolledtext.ScrolledText(form, height=18, state="disabled", bg="#0f141c", fg="#d9e2ef", insertbackground="#fff", relief="flat")
        self.log.grid(row=9, column=0, columnspan=2, sticky="nsew")
        form.rowconfigure(9, weight=1)
        root.protocol("WM_DELETE_WINDOW", self.quit)

    def field(self, parent, label, row, value):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=3)
        item = ttk.Entry(parent); item.grid(row=row, column=1, sticky="ew", pady=3); item.insert(0, value)
        return item

    def write(self, text):
        self.log.configure(state="normal"); self.log.insert("end", f"{time.strftime('%H:%M:%S')}  {text}\n"); self.log.see("end"); self.log.configure(state="disabled")

    def config(self):
        try:
            result = Settings(self.symbol.get().strip(), float(self.lot.get()), float(self.profit.get()), float(self.loss.get()), execute=self.execute.get(), manage_manual=self.manage_manual.get())
            if result.lot <= 0 or result.profit_target < 0 or result.max_loss < 0: raise ValueError
            return result
        except ValueError:
            raise ValueError("Lot must be positive; profit and loss targets cannot be negative.")

    def connect(self):
        try:
            self.settings = self.config()
            if not mt5.initialize(timeout=60000): raise RuntimeError(mt5.last_error())
            if not mt5.symbol_select(self.settings.symbol, True): raise RuntimeError(f"Symbol not found: {self.settings.symbol}")
            account = mt5.account_info()
            if account is None: raise RuntimeError("No active MT5 account.")
            self.connected = True; self.status.set(f"Connected: {account.login} | {account.server} | balance {account.balance:.2f}")
            self.write("Active MT5 session connected. No order sent.")
        except Exception as exc:
            self.connected = False; self.status.set("Connection failed"); self.write(f"Connection error: {exc}")

    def positions(self):
        positions = mt5.positions_get(symbol=self.settings.symbol) or []
        return list(positions) if self.settings.manage_manual else [p for p in positions if p.magic == 26082801]

    def request(self, side, position=None):
        info, tick = mt5.symbol_info(self.settings.symbol), mt5.symbol_info_tick(self.settings.symbol)
        if info is None or tick is None: raise RuntimeError("No live tick for symbol")
        buy = side == "BUY"; price = tick.ask if buy else tick.bid
        typ = mt5.ORDER_TYPE_BUY if buy else mt5.ORDER_TYPE_SELL
        return {"action": mt5.TRADE_ACTION_DEAL, "symbol": self.settings.symbol, "volume": self.settings.lot if position is None else position.volume, "type": typ, "price": price, "deviation": 20, "magic": 26082801, "comment": "mt5-auto-trader", "type_filling": mt5.ORDER_FILLING_IOC, **({"position": position.ticket} if position else {})}

    def preflight(self):
        if not self.connected: self.write("Connect MT5 first."); return
        try:
            check = mt5.order_check(self.request("BUY")); self.write(f"Preflight: {check}")
        except Exception as exc: self.write(f"Preflight error: {exc}")

    def manual(self, side):
        if not self.connected or not self.execute.get(): self.write("Blocked: connect and tick Execute orders first."); return
        try:
            result = mt5.order_send(self.request(side)); self.write(f"{side} result: {result}")
        except Exception as exc: self.write(f"Order error: {exc}")

    def close_all(self):
        if not self.connected or not self.execute.get(): self.write("Blocked: connect and tick Execute orders first."); return
        for p in self.positions():
            result = mt5.order_send(self.request("SELL" if p.type == mt5.POSITION_TYPE_BUY else "BUY", p)); self.write(f"Close {p.ticket}: {result}")

    def manage(self):
        active = self.positions(); pnl = sum(p.profit for p in active)
        if active and ((self.settings.profit_target > 0 and pnl >= self.settings.profit_target) or (self.settings.max_loss > 0 and pnl <= -self.settings.max_loss)):
            self.write(f"Exit threshold reached: P/L {pnl:+.2f}"); self.close_all()

    def start(self):
        if not self.connected: self.write("Connect MT5 first."); return
        self.settings = self.config(); self.running = True; self.stop_event.clear(); self.write("Auto manager started."); threading.Thread(target=self.loop, daemon=True).start()

    def loop(self):
        while not self.stop_event.is_set():
            try: self.manage()
            except Exception as exc: self.write(f"Cycle error: {exc}")
            self.stop_event.wait(self.settings.poll_seconds)

    def stop(self): self.running = False; self.stop_event.set(); self.write("Auto manager stopped.")
    def quit(self): self.stop(); mt5.shutdown(); self.root.destroy()


def main() -> None:
    """Launch the local desktop controller."""
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
