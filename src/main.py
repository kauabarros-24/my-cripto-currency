import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from src.blockchain import Blockchain
from flask import Flask, jsonify
import requests



app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blc = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blc.last_block
    last_proof = last_block['proof']
    proof = blc.proof_of_work(last_proof)

    blc.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = blc.hash(last_block)
    block = blc.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200
    
@app.route("/transaction", methods=['POST'])
def new_transaction():
    return "We'll add a new transaction"

@app.route("/chain", methods=["GET"])
def chain() -> dict:
    response = {
        "chain": blc.chain,
        "len": len(blc.json)
    }
    return jsonify(response), 200
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)