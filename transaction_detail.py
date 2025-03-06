class TransactionDetail:
    """Records the transaction detail of each transaction."""
    def __init__(
            self,
            trans_hash: str = "",
            status: str = "",
            block: int = 0,
            timestamp: str = "",
            method: str = "",
            action: str = "",
            source: str = "",
            target: str = "",
            value: str = "",
            fee: float = 0,
            gas_price: float = 0,
    ):
        self.trans_hash = trans_hash
        self.status = status
        self.block = block
        self.timestamp = timestamp
        self.method = method
        self.action = action
        self.source = source # From
        self.target = target # To
        self.value = value
        self.fee = fee
        self.gas_price = gas_price

    def __str__(self):
        print_string = (f"Transaction Hash: {self.trans_hash}\n"
                        f"Status: {self.status}\n"
                        f"Block: {self.block}\n"
                        f"Timestamp: {self.timestamp}\n"
                        f"Method: {self.method}\n"
                        f"Transaction Action: {self.action}\n"
                        f"From: {self.source}\n"
                        f"To: {self.target}\n"
                        f"Value: {self.value}\n"
                        f"Transaction Fee: {self.fee}\n"
                        f"Gas Price: {self.gas_price}")
        return print_string