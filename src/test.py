import requests
import time

def transaction(url):
    sender = input("Quem envia: ")
    recipient = input("Quem recebe: ")
    amount = float(input(f"Quanto {sender} envia para {recipient}: "))

    data = {
        "sender": sender,
        "recipient": recipient,
        "amount": amount
    }

    print("Gerando transação...")
    time.sleep(0.8)

    response = requests.post(f"{url}/transactions/new", json=data)

    if response.status_code not in [200, 201]:
        print("Erro:", response.text)
        return

    print("✅ Transação criada:")
    print(response.json())


def mine(url):
    print("Minerando bloco...")
    time.sleep(1)

    response = requests.get(f"{url}/mine")

    if response.status_code != 200:
        print("Erro:", response.text)
        return

    print("⛏ Bloco minerado:")
    print(response.json())


def chain(url):
    response = requests.get(f"{url}/chain")

    if response.status_code != 200:
        print("Erro:", response.text)
        return

    print("📦 Blockchain:")
    print(response.json())


def node(url):
    node_address = input("Digite URL do node (ex: http://127.0.0.1:5001): ")

    data = {
        "nodes": [node_address]
    }

    response = requests.post(f"{url}/nodes/register", json=data)

    if response.status_code != 200:
        print("Erro:", response.text)
        return

    print("🌐 Node registrado:")
    print(response.json())


url = input("Digite a URL do node (ex: http://127.0.0.1:8000): ")

response = requests.get(url)

if response.status_code == 200:
    print("✅ Sistema rodando!")

    while True:
        print("\n=== MENU ===")
        print("1 → Nova transação")
        print("2 → Minerar bloco")
        print("3 → Ver blockchain")
        print("4 → Registrar node")
        print("5 → Sair")

        escolha = input("Escolha: ")

        if escolha == "1":
            transaction(url)

        elif escolha == "2":
            mine(url)

        elif escolha == "3":
            chain(url)

        elif escolha == "4":
            node(url)

        elif escolha == "5":
            break

        else:
            print("Opção inválida")

else:
    print("❌ Sistema não está rodando")
        
        