#!/usr/bin/env python3
"""Ghost Trader - MT5 Auto Trade launcher for Kali Linux.

Shows a full-filled saffron (kesari) animated banner, then a solid menu:
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
# ANSI colours (saffron / kesari theme)
# ---------------------------------------------------------------------------
SAFFRON   = "\033[38;2;255;153;51m"
SAFFRON_BG = "\033[48;2;255;153;51m"
GOLD      = "\033[38;2;255;204;102m"
WHITE     = "\033[97m"
DIM       = "\033[90m"
CYAN      = "\033[96m"
GREEN     = "\033[92m"
RED       = "\033[91m"
BLACK_B   = "\033[30;1m"
BOLD      = "\033[1m"
RESET     = "\033[0m"
CLEAR     = "\033[2J\033[H"

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
APP_SCRIPT = os.path.join(BASE_DIR, "mt5_control_app.py")
AUTHOR_URL = "https://github.com/technicalsuraj2"

# Solid filled figlet "banner" art
ART = [
    " #####  #     # #######  #####  ####### ",
    "#     # #     # #     # #     #    #    ",
    "#       #     # #     # #          #    ",
    "#  #### ####### #     #  #####     #    ",
    "#     # #     # #     #       #    #    ",
    "#     # #     # #     # #     #    #    ",
    " #####  #     # #######  #####     #    ",
    "                                     ",
    "####### ######     #    ######  ####### ",
    "   #    #     #   # #   #     # #       ",
    "   #    #     #  #   #  #     # #       ",
    "   #    ######  #     # #     # #####   ",
    "   #    #   #   ####### #     # #       ",
    "   #    #    #  #     # #     # #       ",
    "   #    #     # #     # ######  ####### ",
]

W = max(len(line) for line in ART)
PAD = 4
FULL = W + PAD * 2


def solid_line(text: str = "") -> str:
    """One full-width line with solid saffron background (filled banner)."""
    return f"{SAFFRON_BG}{BLACK_B}{text.ljust(FULL)}{RESET}"


def solid_type(text: str, delay: float = 0.03) -> None:
    """Typewriter on a single filled line (no cursor-up tricks)."""
    sys.stdout.write(solid_line())
    time.sleep(0.05)
    for i in range(1, len(text) + 1):
        sys.stdout.write("\r" + solid_line(text[:i].ljust(len(text))))
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")


def type_banner() -> None:
    print(solid_line())
    for line in ART:
        sys.stdout.write(solid_line(line) + "\n")
        time.sleep(0.04)
    print(solid_line())


def loading_bar(seconds: float = 1.4, width: int = 30) -> None:
    print(f"{DIM}  Initialising Ghost Trading Engine...{RESET}")
    tty = sys.stdout.isatty()
    steps = 40
    for i in range(1, steps + 1):
        done = int(width * i / steps)
        bar = "\u2588" * done + "\u2591" * (width - done)
        pct = int(100 * i / steps)
        line = f"{SAFFRON}  [{bar}]{RESET} {DIM}{pct}%{RESET}"
        if tty:
            sys.stdout.write(f"\r{line}")
        else:
            sys.stdout.write(f"\n{line}")
        sys.stdout.flush()
        time.sleep(seconds / steps)
    done = f"{GREEN}  [{'#' * width}]{RESET} {DIM}100% - Engine ready{RESET}"
    sys.stdout.write(("\r" if tty else "\n") + done + "\n")
    sys.stdout.flush()


def show_banner() -> None:
    print(CLEAR + "\n", end="")
    time.sleep(0.15)
    type_banner()
    time.sleep(0.15)
    print(solid_line("GHOST TRADE"))
    print(solid_line("MT5 AUTO TRADE TERMINAL  |  KALI LINUX  |  KESARI EDITION"))
    print(solid_line())
    print(solid_line())
    loading_bar()
    time.sleep(0.3)
    print(f"{CYAN}  >> Connecting to MetaTrader 5 terminal...{RESET}")
    time.sleep(0.5)


MENU = [
    "",
    "GHOST TRADE  -  MAIN MENU",
    "",
    "   [1]  Start Auto Trade",
    "   [2]  Go to Author Account",
    "   [3]  Exit",
    "",
]


def show_menu() -> int:
    print()
    for line in MENU:
        sys.stdout.write(solid_line(line) + "\n")
        time.sleep(0.04)
    while True:
        choice = input(f"{SAFFRON}ghost-trader > {RESET}").strip()
        if choice in ("1", "2", "3"):
            return int(choice)
        print(f"{RED}  Invalid option. Choose 1, 2 or 3.{RESET}")


def start_auto_trade() -> None:
    print()
    print(f"{GOLD}  Launching MT5 Auto Trade controller in a new window...{RESET}")
    time.sleep(0.6)
    if not os.path.exists(APP_SCRIPT):
        print(f"{RED}  [!] Control app not found: {APP_SCRIPT}{RESET}")
        return
    try:
        subprocess.Popen(
            [sys.executable, APP_SCRIPT],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        print(f"{GREEN}  [+] Auto Trade opened. Switch to the new window/tab and connect MT5.{RESET}")
    except Exception as exc:
        print(f"{RED}  [!] Could not launch control app: {exc}{RESET}")


def go_to_author() -> None:
    print()
    print(f"{GOLD}  Opening author account -> {AUTHOR_URL}{RESET}")
    time.sleep(0.5)
    try:
        webbrowser.open(AUTHOR_URL)
        print(f"{GREEN}  [+] Redirected to author GitHub.{RESET}")
    except Exception as exc:
        print(f"{RED}  [!] Could not open browser: {exc}{RESET}")
        print(f"{CYAN}  Visit: {AUTHOR_URL}{RESET}")


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
                print(f"{DIM}  Exiting Ghost Trader. Goodbye!{RESET}")
                time.sleep(0.6)
                print(CLEAR, end="")
                break
    except KeyboardInterrupt:
        print(f"\n{SAFFRON}Interrupted. Exiting Ghost Trader.{RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()