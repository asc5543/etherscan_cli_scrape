

class TransactionDetail:
    """Records the transaction detail of each transaction."""
    def __init__(self):
        self.trans_hash = ""
        self.status = ""
        self.block = ""
        self.timestamp = ""
        self.action = ""
        self.sponsored = ""
        self.source = "" # From
        self.target = "" # To
        self.value = ""
        self.fee = ""
        self.gas_price = ""
