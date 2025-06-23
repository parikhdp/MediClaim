from flask import Flask, request, jsonify
from web3 import Web3
import ipfshttpclient
import tenseal as ts
from config import w3, contract_instance, INSURER_ADDRESS, INSURER_PRIVATE_KEY, PATIENT_ADDRESS, PATIENT_PRIVATE_KEY, HOSPITAL_ADDRESS, HOSPITAL_PRIVATE_KEY

app = Flask(__name__)
client = ipfshttpclient.connect()



def create_ckks_context(secret=True):
    ctx = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    ctx.global_scale = 2 ** 40
    if secret:
        ctx.generate_galois_keys()
        ctx.generate_relin_keys()
    return ctx

def encrypt_cost(cost: float):
    ctx = create_ckks_context(secret=True)
    enc_vector = ts.ckks_vector(ctx, [cost])
    encrypted_cost = enc_vector.serialize()
    context_with_secret = ctx.serialize(save_secret_key=True)
    return encrypted_cost, context_with_secret

def evaluate_reimbursement(encrypted_data: bytes, context_data: bytes, rate: float = 0.8):
    ctx = ts.context_from(context_data)
    enc_vector = ts.ckks_vector_from(ctx, encrypted_data)
    result_vector = enc_vector * rate
    return result_vector.serialize()

def decrypt_result(encrypted_result: bytes, context_data: bytes):
    ctx = ts.context_from(context_data)
    enc_vector = ts.ckks_vector_from(ctx, encrypted_result)
    return enc_vector.decrypt()[0]



def upload_to_ipfs(data: bytes) -> str:
    return client.add_bytes(data)

def download_from_ipfs(ipfs_hash: str) -> bytes:
    return client.cat(ipfs_hash)



@app.route("/submit_claim", methods=["POST"])
def submit_claim():
    data = request.get_json()
    claim_id = data["claim_id"]
    cost = data["cost"]
    patient = data["patient"]

    encrypted_cost, context_with_secret = encrypt_cost(float(cost))
    cost_ipfs_hash = upload_to_ipfs(encrypted_cost)
    context_ipfs_hash = upload_to_ipfs(context_with_secret)

    nonce = w3.eth.get_transaction_count(HOSPITAL_ADDRESS)
    txn = contract_instance.functions.submitClaim(claim_id, patient, HOSPITAL_ADDRESS, cost_ipfs_hash).build_transaction({
        'from': HOSPITAL_ADDRESS,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': w3.to_wei('20', 'gwei')
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=HOSPITAL_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)

    return jsonify({
        "message": "Claim submitted",
        "tx_hash": tx_hash.hex(),
        "cost_ipfs_hash": cost_ipfs_hash,
        "context_ipfs_hash": context_ipfs_hash
    })

@app.route("/approve_claim_by_patient", methods=["POST"])
def approve_claim_by_patient():
    data = request.get_json()
    claim_id = data["claim_id"]
    nonce = w3.eth.get_transaction_count(PATIENT_ADDRESS)
    txn = contract_instance.functions.approveClaimByPatient(claim_id).build_transaction({
        'from': PATIENT_ADDRESS,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': w3.to_wei('20', 'gwei')
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PATIENT_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return jsonify({"message": "Patient approved the claim", "tx_hash": tx_hash.hex()})

@app.route("/approve_claim", methods=["POST"])
def approve_claim():
    data = request.get_json()
    claim_id = data["claim_id"]
    nonce = w3.eth.get_transaction_count(INSURER_ADDRESS)
    txn = contract_instance.functions.approveClaim(claim_id).build_transaction({
        'from': INSURER_ADDRESS,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': w3.to_wei('20', 'gwei')
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=INSURER_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return jsonify({"message": "Claim approved by insurer", "tx_hash": tx_hash.hex()})

@app.route("/mark_paid", methods=["POST"])
def mark_paid():
    data = request.get_json()
    claim_id = data["claim_id"]
    cost_ipfs_hash = data["cost_ipfs_hash"]
    context_ipfs_hash = data["context_ipfs_hash"]

    encrypted_cost = download_from_ipfs(cost_ipfs_hash)
    context = download_from_ipfs(context_ipfs_hash)

    

    try:
        encrypted_reimbursement = evaluate_reimbursement(encrypted_cost, context)

        reimbursement_amount = decrypt_result(encrypted_reimbursement, context)
    except Exception as e:
        print("Evaluation/decryption error:", str(e))
        return jsonify({"error": "Failed to process encrypted data"}), 500

    reimbursement_msg = f"Reimbursed Amount: {round(reimbursement_amount, 2)}"

    nonce = w3.eth.get_transaction_count(INSURER_ADDRESS)
    txn = contract_instance.functions.markAsPaid(claim_id, reimbursement_msg).build_transaction({
        'from': INSURER_ADDRESS,
        'nonce': nonce,
        'gas': 300000,
        'gasPrice': w3.to_wei('20', 'gwei')
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=INSURER_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)

    return jsonify({
        "message": "Payment marked as completed",
        "tx_hash": tx_hash.hex(),
        "reimbursement": reimbursement_msg
    })

@app.route("/get_claim/<claim_id>", methods=["GET"])
def get_claim(claim_id):
    claim = contract_instance.functions.getClaim(claim_id).call()
    return jsonify({
        "patient": claim[0],
        "hospital": claim[1],
        "ipfs_hash": claim[2],
        "patient_approved": claim[3],
        "approved_by_insurer": claim[4],
        "paid": claim[5],
        "reimbursement_message": claim[6]
    })

if __name__ == "__main__":
    app.run(debug=True)
