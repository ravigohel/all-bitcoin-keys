from dataclasses import dataclass
from typing import Optional

@dataclass
class AllKey:
    """Data class representing a Bitcoin key with its addresses and balances"""
    id: str
    private_key: str
    address_uncompressed: str
    address_uncompressed_balance: Optional[int] = None
    address_uncompressed_received: Optional[int] = None
    address_compressed: str = ""
    address_compressed_balance: Optional[int] = None
    address_compressed_received: Optional[int] = None
