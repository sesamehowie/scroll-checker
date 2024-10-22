import os
from fake_useragent import UserAgent
from pathlib import Path
from loguru import logger
from itertools import cycle
from utils.helpers import read_txt, write_csv
from checker.checker import Checker

cwd = os.getcwd()

private_keys = read_txt(os.path.join(cwd, Path("data/private_keys.txt")))

proxies = read_txt(filename=os.path.join(cwd, Path("data/proxies.txt")))


proxy_cycle = cycle(proxies)


def run_account(account_name, private_key, proxy):
    user_agent = UserAgent(os="windows", min_version=120.0, browsers=["chrome"]).random
    checker = Checker(
        account_name=account_name,
        private_key=private_key,
        proxy=proxy,
        user_agent=user_agent,
    )

    while True:
        try:
            result = checker.check_allocation()
            break
        except Exception as e:
            logger.warning(f"Error: {e}")

    return result


def main():
    i = 1

    results = []
    for private_key in private_keys:
        account_name = str(i)
        proxy = next(proxy_cycle)

        res = run_account(
            account_name=account_name, private_key=private_key, proxy=proxy
        )

        results.append(res)

        i += 1

    if results:
        write_csv(
            file_name=os.path.join(cwd, Path("data/results.csv")),
            data=results,
            header=["account_num", "address", "SCR tokens"],
        )


if __name__ == "__main__":
    main()
