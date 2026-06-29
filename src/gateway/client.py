from dataclasses import dataclass
from datetime import datetime
from codecs import StreamWriter

@dataclass
class Client:
    writer:StreamWriter
    connected_at:datetime.now
    msgs_count:0