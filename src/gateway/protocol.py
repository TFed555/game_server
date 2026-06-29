def protocol(data: str) -> str:
    length = len(data).to_bytes(4, 'big')
    return length