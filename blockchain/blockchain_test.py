import json
from web3 import Web3, exceptions

infura_url = "https://sepolia.infura.io/v3/7b10c7ba73db47deac3f82c84bd00a94"

import os  
from dotenv import load_dotenv

load_dotenv()  

web3 = Web3(Web3.HTTPProvider(infura_url))

abi = json.load(open("abi.json"))
address = "0x1550D992E141de0B772fE98f696F2676Ba0EFD60"
contract = web3.eth.contract(abi=abi, address=address)
# print(contract.functions.getBalance("0x5233862f7245CB0d76af46716631abFB389163C0").call())