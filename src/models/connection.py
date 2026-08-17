from dataclasses import dataclass
from datetime import datetime
import asyncio
from typing import Optional

@dataclass
class Connection:
    id:str
    writer:asyncio.StreamWriter
    reader:asyncio.StreamReader
    connected_at:datetime
    last_act:datetime
    task: asyncio.Task
