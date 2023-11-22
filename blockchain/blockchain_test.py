import json
from web3 import Web3, exceptions

infura_url = "https://sepolia.infura.io/v3/7b10c7ba73db47deac3f82c84bd00a94"

import os  
from dotenv import load_dotenv

load_dotenv()  
  
private_key = input("Private Key: ").strip()
from_account = "0x5233862f7245CB0d76af46716631abFB389163C0"
to_account = "0xf9a568f094FEb5cfD453F1e8e13dfdbe55323B77"
web3 = Web3(Web3.HTTPProvider(infura_url))  
  
try:
    from_account = web3.to_checksum_address(from_account)  
except exceptions.InvalidAddress:  
    print(f"Invalid 'from_account' address: {from_account}")  
  
try:  
    to_account = web3.to_checksum_address(to_account)  
except exceptions.InvalidAddress:  
    print(f"Invalid 'to_account' address: {to_account}")  
  
nonce = web3.eth.get_transaction_count(from_account)  
tx = {
    'type': '0x2',
    'nonce': nonce,
    'from': from_account,
    'to': to_account,
    'value': web3.to_wei(0.00001, 'ether'),
    'maxFeePerGas': web3.to_wei('250', 'gwei'),
    'maxPriorityFeePerGas': web3.to_wei('3', 'gwei'),
    'chainId': 11155111
}
gas = web3.eth.estimate_gas(tx)
tx['gas'] = gas
signed_tx = web3.eth.account.sign_transaction(tx, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
print("Transaction hash: " + str(web3.to_hex(tx_hash)))


abi = json.load(open("abi.json"))
address = "0xf9a568f094FEb5cfD453F1e8e13dfdbe55323B77"
contract = web3.eth.contract(abi=abi, address=address)
print(contract.functions.getBalance("0x5233862f7245CB0d76af46716631abFB389163C0").call())