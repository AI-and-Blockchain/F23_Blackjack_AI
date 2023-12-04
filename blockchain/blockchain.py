import json
from web3 import Web3
from dotenv import load_dotenv
from time import sleep

# class that interfaces to the read only functions of our smart contract
class BlockchainInterface():
    def __init__(self, address):
        # api url to interact with the sepolia eth network
        self.infura_url = "https://sepolia.infura.io/v3/7b10c7ba73db47deac3f82c84bd00a94" 

        # link the instance
        self.web3 = Web3(Web3.HTTPProvider(self.infura_url))

        # load the abi and address of the contract
        abi = json.load(open("blockchain/abi.json"))
        self.address = address
        # connect to the smart contracy
        self.contract = self.web3.eth.contract(abi=abi, address=address)
    
    # queries the balance of a user in the contract
    def getBalance(self, user):
        return self.contract.functions.getBalance(Web3.to_checksum_address(user)).call()
    
    # checks the status of a blockchain transaction, waits for it to be done, and returns when it is
    async def watchForTransaction(self, address):
        while True:
            try:
                # if this fails, the transaction is not finished
                self.web3.eth.get_transaction_receipt(address)
            except:
                # pause so that we aren't infinitely polling
                sleep(1)
                continue
            return True
    
    # converts a given function name to keecak encoded hex (taking only the 8 most significant bytes)
    # function looks like this: func(argtype1,argtype2)
    # this is the same encoding that is used to define function selectors in the compilation of a contract
    # this is used to select a function in a signed transaction
    def getByteCode(self, func):
        return Web3.to_hex(Web3.keccak(text=func))[:10]