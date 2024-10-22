import json
from loguru import logger
from eth_account import Account
from eth_typing import HexStr
from checker.request_client import RequestClient


class Checker(RequestClient):
    def __init__(
        self,
        account_name: str | int,
        private_key: str | HexStr,
        proxy: str,
        user_agent: str,
    ):
        super().__init__(proxy=proxy, user_agent=user_agent)

        self.account_name = account_name
        self.private_key = private_key
        self.address = Account.from_key(private_key).address
        self.user_agent = user_agent
        self.proxy = proxy

    def check_allocation(self):
        logger.info(
            f"{self.account_name} | {self.address} | Checking $SCR allocation..."
        )
        url = "https://claim.scroll.io/?step=1"

        payload = [self.address]

        headers = headers = {
            "accept": "text/x-component",
            "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
            "content-type": "text/plain;charset=UTF-8",
            "next-action": "2ab5dbb719cdef833b891dc475986d28393ae963",
            "next-router-state-tree": "%5B%22%22%2C%7B%22children%22%3A%5B%22(claim)%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2F%3Fstep%3D1%22%2C%22refresh%22%5D%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D",
            "origin": "https://claim.scroll.io",
            "priority": "u=1, i",
            "referer": "https://claim.scroll.io/?step=1",
            "sec-ch-ua": '"Google Chrome";v="120", "Not=A?Brand";v="8", "Chromium";v="120"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-site": "same-origin",
            "user-agent": self.user_agent,
        }

        res = self.html_post(url=url, json=payload, headers=headers)

        data = json.loads(res.text.split("1:")[1].strip())

        return [
            self.account_name,
            self.address,
            round(float(data["amount"]) / 10**18, 4),
        ]
