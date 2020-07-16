def generate_hash(string: str) -> str:
    return abs(hash(string)) % (10 ** 8)
