# MedicalInsuranceSystem
Blockchain-Integrated Privacy-Preserving Medical Insurance Claim Processing Using Homomorphic Encryption.
Project under Dr. Aswani Kumar Cherukuri.
BITE401L-Network and Information Security
We have develop a decentralized medical insurance claim processing system that integrates blockchain and homomorphic encryption to ensure privacy, security, and efficiency. The system will allow patients to submit encrypted medical records to insurance providers, enabling them to verify claims and compute reimbursements without decrypting sensitive data.
1.	Patient visits hospital.
2.	Hospital encrypts the cost using CKKS (HE).
3.	Encrypted cost gets uploaded to IPFS.
4.	Smart contract records claim and IPFS hash.
5.	Patient and insurer approve claim via the UI.
6.	Insurer downloads encrypted cost and evaluates reimbursement over encrypted data.
7.	Result is decrypted and marked as paid via smart contract.
8.	Any user can query claim status


