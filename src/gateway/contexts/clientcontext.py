from dataclasses import dataclass
from datetime import datetime
import asyncio
from typing import Optional

@dataclass
class ClientContext:
    connection_id:str
    # reader:asyncio.StreamReader
    # writer:asyncio.StreamWriter
    last_act:datetime
    client_id:Optional[str] = None
