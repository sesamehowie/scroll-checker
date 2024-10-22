import os
import json
from pathlib import Path
from itertools import cycle
from utils.helpers import read_txt

CWD = os.getcwd()

PRIVATE_KEYS = read_txt(os.path.join(CWD, Path("data/private_keys.txt")))


PROXIES = read_txt(filename=os.path.join(CWD, Path("data/proxies.txt")))

DEPOSIT_ADDRESSES = read_txt(
    filename=os.path.join(CWD, Path("data/deposit_addresses.txt"))
)

PROXY_CYCLE = cycle(PROXIES)

SCROLL_CLAIM_ADDR = "0xE8bE8eB940c0ca3BD19D911CD3bEBc97Bea0ED62"
SCR_TOKEN_ADDR = "0xd29687c813D741E2F938F4aC377128810E217b1b"

ERC20_ABI = json.load(open(os.path.join(CWD, Path("data/abis/erc20.json"))))
CLAIM_ABI = json.load(open(os.path.join(CWD, Path("data/abis/scr_claimer.json"))))
SCR_ABI = json.load(open(os.path.join(CWD, Path("data/abis/scr_token.json"))))
