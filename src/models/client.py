from dataclasses import dataclass
from datetime import datetime
from codecs import StreamWriter
from typing import Optional

@dataclass
class Client:
    id: str
    writer:StreamWriter
    connected_at:datetime
    pending_request:Optional[str] = None
    chatter_id:Optional[str]=None
    msgs_count:int = 0