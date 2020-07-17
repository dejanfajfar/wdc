import secrets


def generate_hash(string: str) -> str:
    return secrets.token_hex(4)
