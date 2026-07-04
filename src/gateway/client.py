from dataclasses import dataclass
from datetime import datetime
from codecs import StreamWriter, StreamReader
from enum import Enum
from typing import Optional

class Mode(Enum):
    Echo = 0
    Chat = 1

@dataclass
class Client:
    writer:StreamWriter
    reader:StreamReader
    connected_at:datetime
    pending_request:Optional[str] = None
    chatter_id:Optional[str]=None
    mode:Optional[Mode]=None
    msgs_count:int = 0