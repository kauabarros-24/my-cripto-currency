from uuid import uuid4
from fastapi import FastAPI, Body
from src.blockchain import Blockchain

app = FastAPI()

node_identifier = str(uuid4()).replace("-", "")
blc = Blockchain()


@app.get("/")
def root():
    return {"message": "System running"}


@app.get("/mine")
def mine():
    last_block = blc.last_block
    last_proof = last_block["proof"]

    proof = blc.proof_of_work(last_proof)

    blc.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = blc.hash(last_block)
    block = blc.new_block(proof, previous_hash)

    response = {
        "message": "New Block Forged",
        "index": block["index"],
        "transactions": block["transactions"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }

    return response


@app.post("/transaction")
def new_transaction(sender: str = Body(...), recipient: str = Body(...), amount: float = Body(...)):
    index = blc.new_transaction(sender, recipient, amount)

    return {
        "message": f"Transaction will be added to Block {index}"
    }


@app.get("/chain")
def chain():
    response = {
        "chain": blc.chain,
        "len": len(blc.chain) 
    }

    return response