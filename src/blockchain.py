import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transaction = []
    
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transcations': self.current_transaction,
            'proof': proof,
        }
        self.current_transactions = []

        self.chain.append(block)
        return block
        
    
    def new_transaction(self, sender, recipient, amount):
        self.current_transaction({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block['index'] + 1
    

 
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode
        return hashlib.sha256(block_string).hexdigest

    @property
    def last_block(self):
        return self.chain[-1]