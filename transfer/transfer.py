from web3 import Web3
from typing import Self
from eth_typing import HexStr, ChecksumAddress
from eth_account import Account
from claimer.evm_client import EvmClient
from utils.networks import Network
from config import SCR_ABI, SCR_TOKEN_ADDR
from utils.decorators import retry


class Transfer(EvmClient):
    def __init__(
        self,
        account_name: str | int,
        private_key: str | HexStr,
        network: Network,
        user_agent: str,
        proxy: str,
    ) -> Self:
        super().__init__(
            account_name=account_name,
            private_key=private_key,
            network=network,
            user_agent=user_agent,
            proxy=proxy,
        )

        self.account_name = account_name
        self.private_key = private_key
        self.network = network
        self.user_agent = user_agent
        self.proxy = proxy
        self.account = Account.from_key(private_key)
        self.address = self.account.address

        self.contract = self.get_contract(
            contract_addr=Web3.to_checksum_address(SCR_TOKEN_ADDR), abi=SCR_ABI
        )

    @retry
    def transfer_to_deposit(self, deposit_address: str | ChecksumAddress) -> bool:
        self.logger.info(
            f"{self.account_name} | {self.address} | Transferring to deposit address {deposit_address}..."
        )

        to_addr = Web3.to_checksum_address(deposit_address)

        balance = self.contract.functions.balanceOf(self.address).call()

        tx_params = self.contract.functions.transfer(
            to_addr, balance
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
