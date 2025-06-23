from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    claim_id = db.Column(db.String(120), unique=True)
    patient_address = db.Column(db.String(120))
    hospital_address = db.Column(db.String(120))
    encrypted_data_ipfs = db.Column(db.String(120))
    context_data = db.Column(db.LargeBinary)  # Patient's context
    reimbursed_data = db.Column(db.LargeBinary)
    payment_status = db.Column(db.String(50), default="Pending")
    status = db.Column(db.String(50), default="Submitted")
