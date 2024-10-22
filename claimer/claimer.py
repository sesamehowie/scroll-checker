from web3 import Web3
from typing import Self
from eth_typing import HexStr
from checker.checker import Checker
from claimer.evm_client import EvmClient
from utils.networks import Network
from eth_account import Account
from config import CLAIM_ABI, SCROLL_CLAIM_ADDR
from utils.decorators import retry


class Claimer(EvmClient, Checker):
    def __init__(
        self,
        account_name: str | int,
        private_key: str | HexStr,
        network: Network,
        user_agent: str,
        proxy: str,
    ) -> Self:
        EvmClient.__init__(
            self,
            account_name=account_name,
            private_key=private_key,
            network=network,
            proxy=proxy,
            user_agent=user_agent,
        )
        Checker.__init__(
            self,
            account_name=account_name,
            private_key=private_key,
            proxy=proxy,
            user_agent=user_agent,
        )

        self.account_name = account_name
        self.private_key = private_key
        self.network = network
        self.user_agent = user_agent
        self.proxy = proxy
        self.account = Account.from_key(private_key)
        self.address = self.account.address
        self.contract = self.get_contract(
            contract_addr=Web3.to_checksum_address(SCROLL_CLAIM_ADDR), abi=CLAIM_ABI
        )

    @retry
    def claim(self):
        self.logger.info(f"{self.account_name} | {self.address} | Starting claim...")

        data = self.check_allocation()

        amount = int(data["amount"])
        merkle_proof = data["proof"]

        tx_params = self.contract.functions.claim(
            self.address, amount, merkle_proof
        ).build_transaction(
            {
                "from": self.address,
                "value": 0,
                "chainId": self.network.chain_id,
                "nonce": self.w3.eth.get_transaction_count(self.address),
            }
        )

        signed = self.sign_transaction(tx_dict=tx_params)

        if signed:
            tx_hash = self.send_tx(signed_tx=signed)

            if tx_hash:
                return True
            return False

        return False
