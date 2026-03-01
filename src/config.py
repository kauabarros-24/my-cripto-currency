from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
llm = None

def get_text_model():
    global llm
    if llm is None:
        print("Carregando modelo de texto...")
        try:
            model_path = hf_hub_download(
                repo_id="KaliumPotas/KaliumKwenModel",
                filename="qwen.gguf"
            )
            llm = Llama(
                model_path=model_path,
                n_ctx=2048,
                n_threads=os.cpu_count() // 2,
                verbose=False
            )
            print("Modelo de texto carregado!")
        except Exception as e:
            print(f"Erro ao carregar modelo de texto: {e}")
            llm = None
    return llm