import ipfshttpclient
from web3 import Web3
from config import WEB3_PROVIDER_URL, CONTRACT_ADDRESS, CONTRACT_ABI

# Initialize Web3
web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Initialize IPFS client
client = ipfshttpclient.connect("/ip4/127.0.0.1/tcp/5001/http")

def upload_to_ipfs(data):
    """ Upload encrypted data to IPFS and return the CID """
    ipfs_hash = client.add_str(data)
    return ipfs_hash

def submit_claim_to_blockchain(patient_address, hospital_address, encrypted_data_ipfs, account):
    """ Submit claim data to the blockchain """
    txn = contract.functions.submitClaim(patient_address, hospital_address, encrypted_data_ipfs).buildTransaction({
        'from': account,
        'gas': 1000000,
        'gasPrice': web3.toWei('20', 'gwei'),
        'nonce': web3.eth.getTransactionCount(account),
    })
    signed_txn = web3.eth.account.signTransaction(txn, private_key="YOUR_PRIVATE_KEY")
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return txn_hash
