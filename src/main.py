from uuid import uuid4
from fastapi import FastAPI, HTTPException
from huggingface_hub import InferenceClient
from pydantic import BaseModel
from src.blockchain import Blockchain
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_text_model


app = FastAPI(title="Blockchain Node")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

node_identifier = str(uuid4()).replace("-", "")

blc = Blockchain()

MODEL_REPO = "KaliumPotas/KaliumKwenModel"

client = InferenceClient(
    model=MODEL_REPO,
    token=None
)

class Prompt(BaseModel):
    prompt: str
class TransactionModel(BaseModel):
    sender: str
    recipient: str
    amount: float

class NodesModel(BaseModel):
    nodes: list[str]

@app.get("/")
def root():
    return {"message": "Blockchain node running"}

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

    return {
        "message": "New Block Forged",
        "block": block,
    }

@app.post("/transactions/new")
def new_transaction(transaction: TransactionModel):
    index = blc.new_transaction(
        transaction.sender,
        transaction.recipient,
        transaction.amount
    )

    return {
        "message": f"Transaction will be added to Block {index}"
    }

@app.get("/chain")
def full_chain():
    return {
        "chain": blc.chain,
        "length": len(blc.chain)
    }

@app.post("/nodes/register")
def register_nodes(data: NodesModel):
    if not data.nodes:
        raise HTTPException(400, "Lista de nós vazia")

    for node in data.nodes:
        blc.register_node(node)

    return {
        "message": "New nodes added",
        "total_nodes": list(blc.nodes),
    }

@app.get("/nodes/resolve")
def consensus():
    replaced = blc.resolve_conflicts()

    if replaced:
        return {"message": "Chain replaced"}
    else:
        return {"message": "Chain is authoritative"}

@app.get("/generate")
def generate():
    
    data = {
        "prompt": "De uma breve explicação sobre blockchain"
    }
    try:
        model = get_text_model()
        print(model)
        if model is None:
            raise HTTPException(503, "Modelo de texto não disponível")
            
        output = model.create_chat_completion(
            messages=[{"role": "user", "content": data["prompt"]}],
            max_tokens=200,
            temperature=0.7
        )
        
        return output["choices"][0]["message"]["content"].replace('"', "").replace("\n", "")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))