import os
import json
from web3 import Web3

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///medical_claims.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)

    # Blockchain settings
    WEB3_PROVIDER_URL = 'http://127.0.0.1:8545'
    CONTRACT_ADDRESS = ''
    HOSPITAL_ADDRESS = ''
    PRIVATE_KEY = ''
    HOSPITAL_PRIVATE_KEY = ""

    INSURER_ADDRESS = ''
    INSURER_PRIVATE_KEY = ''

    PATIENT_ADDRESS = ""
    PATIENT_PRIVATE_KEY = ""

#Initialize Web3
w3 = Web3(Web3.HTTPProvider(Config.WEB3_PROVIDER_URL))

#Load ABI
abi_path = os.path.join(os.path.dirname(__file__), 'contract_abi.json')
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

# Create contract instance
contract_instance = w3.eth.contract(address=Config.CONTRACT_ADDRESS, abi=contract_abi)

#Export for external use
CONTRACT_ABI = contract_abi
CONTRACT_ADDRESS = Config.CONTRACT_ADDRESS
INSURER_ADDRESS = Config.INSURER_ADDRESS
INSURER_PRIVATE_KEY = Config.INSURER_PRIVATE_KEY
HOSPITAL_PRIVATE_KEY=Config.HOSPITAL_PRIVATE_KEY
PATIENT_ADDRESS=Config.PATIENT_ADDRESS
PATIENT_PRIVATE_KEY=Config.PATIENT_PRIVATE_KEY
HOSPITAL_ADDRESS=Config.HOSPITAL_ADDRESS

