from dataclasses import dataclass
from datetime import datetime
from codecs import StreamWriter, StreamReader
from typing import Optional

@dataclass
class Client:
    id: str
    writer:StreamWriter
    reader:StreamReader
    connected_at:datetime
    last_pong:datetime
    pending_request:Optional[str] = None
    chatter_id:Optional[str]=None
    msgs_count:int = 0
