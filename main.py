import os
from fake_useragent import UserAgent
from pathlib import Path
from loguru import logger
from utils.helpers import write_csv, sleeping
from checker.checker import Checker
from claimer.claimer import Claimer
from transfer.transfer import Transfer
from utils.networks import Network, Networks
from config import PRIVATE_KEYS, PROXY_CYCLE, CWD, DEPOSIT_ADDRESSES


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


def write_results() -> None:
    i = 1

    results = []
    for private_key in PRIVATE_KEYS:
        account_name = str(i)
        proxy = next(PROXY_CYCLE)

        res = [
            account_name,
            private_key,
            round(
                float(
                    run_account(
                        account_name=account_name, private_key=private_key, proxy=proxy
                    )
                )
                / 10**18,
                4,
            ),
        ]

        results.append(res)
        i += 1

    if results:
        write_csv(
            file_name=os.path.join(CWD, Path("data/results.csv")),
            data=results,
            header=["account_num", "address", "SCR tokens"],
        )


def claim_for_account(
    account_name: str | int,
    private_key: str,
    network: Network,
    user_agent: str,
    proxy: str,
) -> bool:
    claimer = Claimer(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return claimer.claim()


def claim():
    i = 0
    for private_key in PRIVATE_KEYS:
        account_name = str(i)
        proxy = next(PROXY_CYCLE)
        network = Networks.Scroll
        user_agent = UserAgent(
            os="windows", min_version=120.0, browsers=["chrome"]
        ).random

        claim_for_account(
            account_name=account_name,
            private_key=private_key,
            network=network,
            user_agent=user_agent,
            proxy=proxy,
        )
        i += 1
        sleeping(1)


def transfer_for_account(
    account_name: str | int,
    private_key: str,
    network: Network,
    user_agent: str,
    proxy: str,
    deposit_address: str,
):
    transfer = Transfer(
        account_name=account_name,
        private_key=private_key,
        network=network,
        user_agent=user_agent,
        proxy=proxy,
    )

    return transfer.transfer_to_deposit(deposit_address=deposit_address)


def transfer():
    i = 1
    for private_key, deposit_address in list(zip(PRIVATE_KEYS, DEPOSIT_ADDRESSES)):
        account_name = str(i)
        proxy = next(PROXY_CYCLE)
        network = Networks.Scroll
        user_agent = UserAgent(
            os="windows", min_version=120.0, browsers=["chrome"]
        ).random

        transfer_for_account(
            account_name=account_name,
            private_key=private_key,
            network=network,
            user_agent=user_agent,
            proxy=proxy,
            deposit_address=deposit_address,
        )
        i += 1
        sleeping(1)


def main():
    task_mapping = {1: write_results, 2: claim, 3: transfer}

    inp = int(
        input(
            "Enter what to do:\n1. Check allocation and write to file.\n2. Claim allocation\n3. Transfer to CEX deposit accountss\n"
        )
    )

    return task_mapping[inp]()


if __name__ == "__main__":
    main()
