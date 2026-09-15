#!/usr/bin/env python3
"""Ghost Trader - MT5 Auto Trade launcher for Kali Linux.

Clean, normal kesari (saffron) text launcher - no background fills, no
cursor tricks, so the output is always clean and readable:

    [1]  Start Auto Trade    -> opens the MT5 control app in a new window
    [2]  Go to Author        -> opens the author's GitHub in the browser
    [3]  Exit
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
import webbrowser

# ---------------------------------------------------------------- colours ---
SAFFRON = "\033[38;2;255;153;51m"   # kesari (saffron) - text colour only
GOLD    = "\033[38;2;255;204;102m"
WHITE   = "\033[97m"
CYAN    = "\033[96m"
GREEN   = "\033[92m"
RED     = "\033[91m"
DIM     = "\033[90m"
BOLD    = "\033[1m"
RESET   = "\033[0m"
CLEAR   = "\033[2J\033[H"

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
APP_SCRIPT = os.path.join(BASE_DIR, "mt5_control_app.py")
AUTHOR_URL = "https://github.com/technicalsuraj2"

# -------------------------------------------------------------------- art ---
# Plain ASCII banner (standard figlet) - always readable
ART = [
    "  ######  #######  #####  #######  #####           #####   ",
    " #     #   #     # #     # #     # #     #         #     #  ",
    " #          #     # #       #     # #              #       ",
    "  #####     #     #  #####  #######  #####         #  #### ",
    "       #    #     #       # #     #       #        #     # ",
    " #     #    #     # #     # #     # #     #        #     # ",
    "  #####   #######  #####  #######  #####           #####  ",
    "                                                          ",
    "   ######  #######   #####   #####  #######   #####      ",
    "   #     #    #       #     #       #       #     #      ",
    "   #          #       #     #       #       #            ",
    "   #          #        #####  #####  #####    #####      ",
    "   #          #            #       # #              #    ",
    "   #     #    #       #     # #     # #        #     #   ",
    "   ######   #######   #####   #####  #######  #####     ",
]
TITLE_LINE = "GHOST TRADE  -  MT5 AUTO TRADE TERMINAL  |  KALI LINUX  |  KESARI EDITION"


# ---------------------------------------------------------------- helpers ---
def cprint(text: str, colour: str = WHITE, bold: bool = False) -> None:
    sys.stdout.write(f"{BOLD if bold else ''}{colour}{text}{RESET}\n")


def type_line(text: str, delay: float = 0.02, colour: str = SAFFRON) -> None:
    for ch in text:
        sys.stdout.write(colour + ch if ch != " " else ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(RESET)
    sys.stdout.write("\n")
    sys.stdout.flush()


def show_banner() -> None:
    sys.stdout.write(CLEAR)
    sys.stdout.flush()
    time.sleep(0.1)
    for line in ART:
        type_line(line)
    time.sleep(0.1)
    cprint(TITLE_LINE, GOLD, bold=True)
    time.sleep(0.2)


def loading_bar(seconds: float = 1.4, width: int = 32) -> None:
    print(f"{DIM}   Initialising Engine...{RESET}")
    steps = 24
    for i in range(1, steps + 1):
        done = int(width * i / steps)
        bar = "=" * done + "." * (width - done)
        pct = int(100 * i / steps)
        print(f"{SAFFRON}   [{bar}]{RESET}  {DIM}{pct}%{RESET}")
        sys.stdout.flush()
        time.sleep(seconds / steps)
    print(f"{GREEN}   [{'=' * width}]{RESET}  {DIM}100% - Engine ready{RESET}")


def show_menu() -> int:
    print()
    cprint("   GHOST TRADE  -  MAIN MENU", SAFFRON, bold=True)
    print(f"{SAFFRON}   --------------------------------{RESET}")
    print(f"{GOLD}      [ 1 ]  Start Auto Trade{RESET}")
    print(f"{GOLD}      [ 2 ]  Go to Author Account{RESET}")
    print(f"{GOLD}      [ 3 ]  Exit{RESET}")
    print(f"{SAFFRON}   --------------------------------{RESET}")
    while True:
        choice = input(f"{SAFFRON}ghost-trader > {RESET}").strip()
        if choice in ("1", "2", "3"):
            return int(choice)
        print(f"{RED}   Invalid option. Choose 1, 2 or 3.{RESET}")


def start_auto_trade() -> None:
    print()
    cprint("   Launching MT5 Auto Trade controller in a new window...", GOLD, bold=True)
    time.sleep(0.4)
    if not os.path.exists(APP_SCRIPT):
        cprint(f"   [!] Control app not found: {APP_SCRIPT}", RED)
        return
    try:
        subprocess.Popen(
            [sys.executable, APP_SCRIPT],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
        cprint("   [+] Control app opened in a new window. Connect MT5 there.", GREEN)
    except Exception as exc:
        cprint(f"   [!] Could not launch control app: {exc}", RED)


def go_to_author() -> None:
    print()
    cprint(f"   Opening author account -> {AUTHOR_URL}", GOLD)
    time.sleep(0.3)
    try:
        webbrowser.open(AUTHOR_URL)
        cprint("   [+] Redirected to author account.", GREEN)
    except Exception as exc:
        cprint(f"   [!] Could not open browser: {exc}", RED)
        cprint(f"   Visit: {AUTHOR_URL}", CYAN)


def main() -> None:
    try:
        show_banner()
        loading_bar()
        while True:
            choice = show_menu()
            if choice == 1:
                start_auto_trade()
            elif choice == 2:
                go_to_author()
            else:
                cprint("   Exiting Ghost Trader. Goodbye!", DIM)
                time.sleep(0.5)
                break
    except KeyboardInterrupt:
        print(f"\n{SAFFRON}   Interrupted. Exiting Ghost Trader.{RESET}")
        sys.exit(0)


if __name__ == "__main__":
    main()
