import json
from web3 import Web3
from dotenv import load_dotenv
from time import sleep


class BlockchainInterface():
    def __init__(self, address):
        self.infura_url = "https://sepolia.infura.io/v3/7b10c7ba73db47deac3f82c84bd00a94"

        load_dotenv()  

        self.web3 = Web3(Web3.HTTPProvider(self.infura_url))

        abi = json.load(open("blockchain/abi.json"))
        self.address = address
        self.contract = self.web3.eth.contract(abi=abi, address=address)
    
    def getBalance(self, user):
        return self.contract.functions.getBalance(Web3.to_checksum_address(user)).call()
    
    def payUser(self, user, amount):
        return self.contract.functions.cashOut(Web3.to_checksum_address(user), amount).call()
    
    async def watchForTransaction(self, address):
        while True:
            try:
                self.web3.eth.get_transaction_receipt(address)
            except:
                sleep(1)
                continue
            return True
    
    def getByteCode(self, func):
        return Web3.to_hex(Web3.keccak(text=func))[:10]