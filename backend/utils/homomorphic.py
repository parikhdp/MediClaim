import tenseal as ts

def create_ckks_context(secret=True):
    # Create CKKS encryption context
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
    # Create context and encrypt cost
    ctx = create_ckks_context(secret=True)
    enc_vector = ts.ckks_vector(ctx, [cost])
    encrypted_cost = enc_vector.serialize()
    context_with_secret = ctx.serialize(save_secret_key=True)
    return encrypted_cost, context_with_secret

def evaluate_reimbursement(encrypted_data: bytes, rate: float = 0.8):
    # Evaluate reimbursement homomorphically
    ctx = create_ckks_context(secret=False)
    enc_vector = ts.ckks_vector_from(ctx, encrypted_data)
    result_vector = enc_vector * rate
    return result_vector.serialize()

def decrypt_result(encrypted_result: bytes, context_data: bytes):
    # Decrypt final reimbursement
    ctx = ts.context_from(context_data)
    enc_vector = ts.ckks_vector_from(ctx, encrypted_result)
    return enc_vector.decrypt()[0]
