#!/usr/bin/env python3
"""Ghost Trader - MT5 Auto Trade launcher for Kali Linux.

Runs a saffron (kesari) animated intro banner and then shows a menu:
    1. Start Auto Trade     -> opens the MT5 desktop controller in a new window/tab
    2. Go to Author Account -> opens the author's GitHub in the browser
    3. Exit
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
import webbrowser

# ---------------------------------------------------------------------------
# ANSI colour helpers (saffron / kesari theme)
# ---------------------------------------------------------------------------
SAFFRON = "\033[38;2;255;153;51m"
GOLD    = "\033[38;2;255;204;102m"
WHITE   = "\033[97m"
DIM     = "\033[90m"
CYAN    = "\033[96m"
GREEN   = "\033[92m"
RED     = "\033[91m"
BOLD    = "\033[1m"
RESET   = "\033[0m"
CLEAR   = "\033[2J\033[H"
UP_LINE = "\033[1A\033[2K"

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
APP_SCRIPT = os.path.join(BASE_DIR, "mt5_control_app.py")
AUTHOR_URL = "https://github.com/technicalsuraj2"

# figlet "standard" art (raw string so backslashes stay literal)
BANNER = r"""
  ____ _   _  ___  ____ _____   _____ ____      _    ____  _____ 
 / ___| | | |/ _ \/ ___|_   _| |_   _|  _ \    / \  |  _ \| ____|
| |  _| |_| | | | \___ \ | |     | | | |_) |  / _ \ | | | |  _|  
| |_| |  _  | |_| |___) || |     | | |  _ <  / ___ \| |_| | |___ 
 \____|_| |_|\___/|____/ |_|     |_| |_| \_\/_/   \_\____/|_____|
"""

TITLE = "GHOST TRADE"


def cprint(text: str, colour: str = WHITE, bold: bool = False) -> None:
    print(f"{BOLD if bold else ''}{colour}{text}{RESET}")


def type_line(text: str, delay: float = 0.025, colour: str = SAFFRON) -> None:
    print(colour, end="")
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print(RESET)


def type_banner() -> None:
    for line in BANNER.splitlines():
        type_line(line, delay=0.016)


def loading_bar(seconds: float = 1.6, width: int = 34) -> None:
    print(f"{DIM}   Initialising Ghost Trading Engine...{RESET}\n")
    steps = 40
    for i in range(1, steps + 1):
        done = int(width * i / steps)
        bar = "=" * done + ">" + "-" * (width - done - 1)
        print(f"{SAFFRON}   [{bar}]{RESET} {int(100 * i / steps)}%", end="", flush=True)
        time.sleep(seconds / steps)
        print(UP_LINE, end="")
    print(f"{GREEN}   [{'=' * width}] 100% - Engine ready{RESET}\n")


def show_banner() -> None:
    print(CLEAR + "\n", end="")
    time.sleep(0.15)
    type_banner()
    time.sleep(0.1)
    # pulse the title 3 times
    for _ in range(3):
        cprint(TITLE.center(62), SAFFRON, bold=True)
        time.sleep(0.18)
        print(UP_LINE, end="")
        time.sleep(0.12)
    cprint(TITLE.center(62), SAFFRON, bold=True)
    print()
    print(f"{GOLD}{'~' * 62}{RESET}")
    print(f"{CYAN}   MT5 AUTO TRADE TERMINAL   {DIM}|   Kali Linux Edition{RESET}")
    print(f"{GOLD}{'~' * 62}{RESET}\n")
    loading_bar()
    time.sleep(0.3)
    cprint("   >> Connecting to MetaTrader 5 terminal...", CYAN, bold=True)
    time.sleep(0.5)


def show_menu() -> int:
    print()
    cprint("┌──────────────────────────────────────────────┐", WHITE)
    cprint("            GHOST TRADE  -  MAIN MENU", SAFFRON, bold=True)
    cprint("├──────────────────────────────────────────────┤", WHITE)
    cprint("   [1]  Start Auto Trade", GOLD)
    cprint("   [2]  Go to Author Account", GOLD)
    cprint("   [3]  Exit", GOLD)
    cprint("└──────────────────────────────────────────────┘", WHITE)
    while True:
        choice = input(f"{SAFFRON}ghost-trader > {RESET}").strip()
        if choice in ("1", "2", "3"):
            return int(choice)
        cprint("Invalid option. Choose 1, 2 or 3.", RED)


def start_auto_trade() -> None:
    print()
    cprint("Launching MT5 Auto Trade controller in a new window...", GOLD, bold=True)
    time.sleep(0.6)
    if not os.path.exists(APP_SCRIPT):
        cprint(f"[!] Control app not found: {APP_SCRIPT}", RED)
        return
    try:
        subprocess.Popen(
            [sys.executable, APP_SCRIPT],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        cprint("[+] Auto Trade opened. Switch to the new window/tab and connect MT5.", GREEN)
    except Exception as exc:
        cprint(f"[!] Could not launch control app: {exc}", RED)


def go_to_author() -> None:
    print()
    cprint(f"Opening author account -> {AUTHOR_URL}", GOLD)
    time.sleep(0.5)
    try:
        webbrowser.open(AUTHOR_URL)
        cprint("[+] Redirected to author GitHub.", GREEN)
    except Exception as exc:
        cprint(f"[!] Could not open browser: {exc}", RED)
        cprint(f"    Visit: {AUTHOR_URL}", CYAN)


def main() -> None:
    try:
        show_banner()
        while True:
            choice = show_menu()
            if choice == 1:
                start_auto_trade()
            elif choice == 2:
                go_to_author()
            else:
                cprint("Exiting Ghost Trader. Goodbye!", DIM)
                time.sleep(0.6)
                print(CLEAR, end="")
                break
    except KeyboardInterrupt:
        print(f"\n{SAFFRON}Interrupted. Exiting Ghost Trader.{RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()