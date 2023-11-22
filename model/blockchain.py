import json
from web3 import Web3
from dotenv import load_dotenv


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