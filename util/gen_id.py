from nanoid import generate


def generate_sql_id():
    """Generate id using safe string and length 10"""
    alpha = "6789BCDFGHJKLMNPQRTWbcdfghjkmnpqrtwz"
    return generate(alphabet=alpha, size=10)
