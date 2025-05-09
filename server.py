from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# === Contatos pré-carregados ===
contatos = {
    "lara": {"nome": "Lara", "numero": "+5561xxxxxxxx"},
    "pedro": {"nome": "Pedro", "numero": "+5561xxxxxxxx"},
    "philippe": {"nome": "Philippe", "numero": "+5562xxxxxxxx"}
}

# === Modelo da requisição para a tool ===
class SendMessageRequest(BaseModel):
    numero: str
    mensagem: str

# === Tool send_message ===
@app.post("/tools/send_message")
def send_message(request: SendMessageRequest):
    chat_id = request.numero.replace("+", "") + "@c.us"
    data = {
        "chatId": chat_id,
        "text": request.mensagem,
        "session": "default"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    response = requests.post("http://localhost:3000/api/sendText", json=data, headers=headers)
    return response.json()

# === Resource de contatos ===
@app.get("/resources/contatos")
def listar_contatos():
    return list(contatos.values())

# === Enviar mensagem de bom dia por nome ===
@app.get("/tools/send_message/by_name/{nome}")
def enviar_por_nome(nome: str):
    contato = contatos.get(nome.lower())
    if not contato:
        return {"erro": "Contato não encontrado."}
    mensagem = f"Olá, {contato['nome']}, esta é uma mensagem de teste utilizando um servidor MCP-WAHA. :)"
    return send_message(SendMessageRequest(numero=contato["numero"], mensagem=mensagem))
