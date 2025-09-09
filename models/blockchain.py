from dataclasses import dataclass

@dataclass
class Blockchain:
    """Data class representing blockchain balance information"""
    final_balance: int
    n_tx: int
    total_received: int
