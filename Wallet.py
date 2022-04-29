from web3 import Web3
from eth_account import Account
import hashlib
import secrets


passw = secrets.token_hex(32)
private_key = "0x"+passw
print(f"{private_key} This is the Password don't share this")
acct = Account.from_key(private_key)
print("Address:", acct.address)

infura_url ="https://kovan.infura.io/v3/1b6c0ac430c04d9ea18aabe4d787763d"
web3 = Web3(Web3.HTTPProvider(infura_url))
print(web3.isConnected())
print(web3.eth.blockNumber)



# from secrets import token_bytes
# from web3 import Web3
# private_key = keccak_256(token_bytes(32)).digest()
# public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
# addr = keccak_256(public_key).digest()[-20:]

# print('private_key:', private_key.hex())
# print('eth addr: 0x' + addr.hex())
