from web3 import Web3
from config import Config

# Create Web3 instance
w3 = Web3(Web3.HTTPProvider(Config.WEB3_PROVIDER_URL))

# Convert contract address to checksum
contract_address = w3.to_checksum_address(Config.CONTRACT_ADDRESS)

# Initialize contract
contract = w3.eth.contract(
    address=contract_address,
    abi=Config.CONTRACT_ABI
)

def submit_claim_to_blockchain(claim_id, patient, hospital, ipfs_hash, sender):
    # Convert all addresses to checksum format
    patient = w3.to_checksum_address(patient)
    hospital = w3.to_checksum_address(hospital)
    sender = w3.to_checksum_address(sender)

    txn = contract.functions.submitClaim(claim_id, patient, hospital, ipfs_hash).build_transaction({
        "from": sender,
        "nonce": w3.eth.get_transaction_count(sender),
        "gas": 3000000,
        "gasPrice": w3.to_wei("10", "gwei")
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=Config.PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash.hex()
