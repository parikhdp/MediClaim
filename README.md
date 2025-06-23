# 🏥 Mediclaim  
**Mediclaim** is a decentralized medical insurance claim processing system that integrates **Blockchain**, **Homomorphic Encryption (HE)**, and **IPFS** to ensure security, privacy, and trustless verification. Built as a course project under **BITE401L - Network and Information Security**, this system enables patients, hospitals, and insurers to interact securely without compromising sensitive medical data.

---

## ✨ Features  
🔐 **Privacy-Preserving Claims** – Encrypt treatment cost using CKKS and compute over ciphertext  
⛓️ **Blockchain Integration** – Immutable claim tracking via Ethereum smart contracts  
📂 **IPFS Storage** – Decentralized and verifiable storage for encrypted medical records  
🧾 **Multi-Party Approval Flow** – Patients and insurers can approve claims through a web UI  
📈 **Claim Status Monitoring** – Publicly query and view claim status on-chain  
⚙️ **Homomorphic Evaluation** – Insurer can compute reimbursement without decryption  

---

## 🛠️ Tech Stack  

| Technology     | Purpose                                       |
|----------------|-----------------------------------------------|
| Python         | Backend logic and API handling                |
| Flask          | Lightweight web framework                     |
| TenSEAL (CKKS) | Homomorphic encryption for treatment costs    |
| Solidity       | Smart contract implementation on Ethereum     |
| IPFS           | Decentralized file storage                    |
| Web3.py        | Ethereum blockchain interaction               |
| HTML/CSS       | Frontend for patient, hospital, and insurer   |

---

## 📚 What You'll Learn  
- How to implement **homomorphic encryption** using TenSEAL  
- Interfacing **smart contracts** with a Python backend  
- Building a decentralized app (dApp) using **IPFS** and **Web3**  
- Designing multi-role claim approval flows  
- Encrypting data and computing over encrypted values  
- Securing sensitive medical data without sacrificing usability  

---

## 🧪 Project Highlights  
- End-to-end **decentralized medical claim flow** involving hospital, patient, and insurer  
- **Encrypted cost storage** using IPFS with smart contract-based validation  
- **Reimbursement over encrypted data** with decryption-free calculations  
- Multi-party approval with frontend interfaces for all stakeholders  
- Full-stack integration: HE + Blockchain + Smart Contracts + IPFS  

---

## 🚀 Getting Started

To run this project locally, follow these steps:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mediclaim.git
cd mediclaim
````

### 2. Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add the following:

```env
INFURA_URL=<your_infura_or_rpc_url>
PRIVATE_KEY=<your_ethereum_account_private_key>
CONTRACT_ADDRESS=<your_deployed_smart_contract_address>
```

### 5. Start the Flask Backend

```bash
python backend/app.py
```

---

### ✅ Notes

* Make sure Python 3.7 or above is installed.
* If using environment variables via `.env`, install `python-dotenv`:

  ```bash
  pip install python-dotenv
  ```
* To exit the virtual environment at any time, run:

  ```bash
  deactivate
  ```


### 🤝 Contributing

Contributions are welcome! Fork the repo, make your changes, and submit a pull request.


