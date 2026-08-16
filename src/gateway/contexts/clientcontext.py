from dataclasses import dataclass

@dataclass
class ClientContext:
    client_id: str
    last_pong: float
