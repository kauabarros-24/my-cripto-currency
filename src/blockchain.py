import hashlib
import json
from time import time
from urllib.parse import urlparse
import requests

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        self.new_block(proof=100, previous_hash="1")
        
    def register_node(self, address):
        parsed_url=urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f"http://{node}/chain")
            
            if response.status_code == 200:
                lenght = response.json()["lenght"]
                chain = response.json()["chain"]
                
                if lenght > max_length and self.valid_chain[chain]:
                    max_length = lenght
                    new_chain = chain   
                    
        if new_chain:
            self.chain = new_chain
            return True

        return False
    
    def valid_chain(self, chain):
        self.last_block = chain[0]
        current_index = 1
        
        while current_index < len(chain):
            block = chain[current_index]
            
            if block["previous_hash"] != self.hash(self.last_block):
                return False
            
            if not self.valid_proof(last_block["proof"], block["proof"]):
                return False

            last_block = block
            current_index += 1

        return True
            
                
    def new_block(self, proof, previous_hash=None):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "transactions": self.current_transactions,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

        return self.last_block["index"] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0

        while not self.valid_proof(last_proof, proof):
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f"{last_proof}{proof}".encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"