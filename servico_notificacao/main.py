from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI(title="Microsserviço - Notificações")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class NotificacaoPayload(BaseModel):
    cliente: str
    mensagem: str

# Banco de dados em memória para demonstração
historico_notificacoes: List[dict] = []

@app.get("/api/health")
def health():
    return {"status": "online", "servico": "Notificações"}

@app.post("/api/notificar")
def receber_notificacao(payload: NotificacaoPayload):
    print(f"[NOTIFICAÇÃO] Para: {payload.cliente} | Msg: {payload.mensagem}")

    registro = {
        "id": len(historico_notificacoes) + 1,
        "cliente": payload.cliente,
        "mensagem": payload.mensagem,
        "canal": "SMS/Email simulado",
        "status": "enviado",
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    historico_notificacoes.append(registro)

    return {"status": "sucesso", "registro": registro}

@app.get("/api/historico")
def obter_historico():
    return {
        "total": len(historico_notificacoes),
        "historico": list(reversed(historico_notificacoes))
    }

@app.delete("/api/historico")
def limpar_historico():
    historico_notificacoes.clear()
    return {"status": "histórico limpo"}

