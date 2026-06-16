from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from domain.entities import ConfiguracaoOficina
from use_cases.criar_ordem_servico import CriarOrdemServicoUseCase

app = FastAPI(title="Microsserviço - Oficina")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PedidoServicoDTO(BaseModel):
    nome_cliente: str
    veiculo: str
    servico_base: str
    adicionais: List[str]

@app.get("/api/info")
def get_info():
    config = ConfiguracaoOficina()
    return {"oficina": config.nome, "microsservico": "Oficina Core"}

@app.post("/api/ordem-servico")
def criar_ordem(pedido: PedidoServicoDTO):
    use_case = CriarOrdemServicoUseCase()
    try:
        resultado = use_case.executar(
            nome_cliente=pedido.nome_cliente,
            veiculo=pedido.veiculo,
            servico_base=pedido.servico_base,
            adicionais=pedido.adicionais
        )
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
