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
        try:
            parsed_url = urlparse(address)
            if not parsed_url.netloc:
                raise ValueError("Endereço inválido")
            self.nodes.add(parsed_url.netloc)
        except Exception as e:
            print(f"Erro ao registrar node: {e}")

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours:
            try:
                response = requests.get(f"http://{node}/chain", timeout=5)

                if response.status_code != 200:
                    continue

                data = response.json()
                length = data.get("length")
                chain = data.get("chain")

                if not length or not chain:
                    continue

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

            except requests.exceptions.RequestException:
                print(f"Node {node} offline ou inacessível")
            except ValueError:
                print(f"Resposta inválida do node {node}")
            except Exception as e:
                print(f"Erro inesperado com node {node}: {e}")

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def valid_chain(self, chain):
        try:
            last_block = chain[0]
            current_index = 1

            while current_index < len(chain):
                block = chain[current_index]

                if block["previous_hash"] != self.hash(last_block):
                    return False

                if not self.valid_proof(last_block["proof"], block["proof"]):
                    return False

                last_block = block
                current_index += 1

            return True

        except (KeyError, IndexError, TypeError):
            print("Chain inválida ou corrompida")
            return False
        except Exception as e:
            print(f"Erro validando chain: {e}")
            return False

    def new_block(self, proof, previous_hash=None):
        try:
            block = {
                "index": len(self.chain) + 1,
                "timestamp": time(),
                "transactions": self.current_transactions,
                "proof": proof,
                "previous_hash": previous_hash or self.hash(self.chain[-1]) if self.chain else "1",
            }

            self.current_transactions = []
            self.chain.append(block)
            return block

        except Exception as e:
            print(f"Erro criando bloco: {e}")

    def new_transaction(self, sender, recipient, amount):
        try:
            if not sender or not recipient:
                raise ValueError("Sender e recipient obrigatórios")

            if amount <= 0:
                raise ValueError("Amount deve ser positivo")

            self.current_transactions.append({
                "sender": sender,
                "recipient": recipient,
                "amount": amount
            })

            return self.last_block["index"] + 1

        except Exception as e:
            print(f"Erro na transação: {e}")

    @staticmethod
    def hash(block):
        try:
            block_string = json.dumps(block, sort_keys=True).encode()
            return hashlib.sha256(block_string).hexdigest()
        except Exception as e:
            print(f"Erro ao gerar hash: {e}")

    @property
    def last_block(self):
        return self.chain[-1] if self.chain else None

    def proof_of_work(self, last_proof):
        try:
            proof = 0
            while not self.valid_proof(last_proof, proof):
                proof += 1
            return proof
        except Exception as e:
            print(f"Erro no proof of work: {e}")

    @staticmethod
    def valid_proof(last_proof, proof):
        try:
            guess = f"{last_proof}{proof}".encode()
            guess_hash = hashlib.sha256(guess).hexdigest()
            return guess_hash[:4] == "0000"
        except Exception:
            return False