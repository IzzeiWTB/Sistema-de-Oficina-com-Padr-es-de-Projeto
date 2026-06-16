from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Padrão 1: Singleton
class ConfiguracaoOficina:
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConfiguracaoOficina, cls).__new__(cls)
            cls._instancia.nome = "Auto Mecânica Central"
        return cls._instancia

# Interfaces Base
class ServicoAutomotivo(ABC):
    @abstractmethod
    def obter_descricao(self) -> str: pass
    @abstractmethod
    def obter_custo(self) -> float: pass

class ReparoMotor(ServicoAutomotivo):
    def obter_descricao(self): return "Reparo de Motor"
    def obter_custo(self): return 1500.00

class ReparoSuspensao(ServicoAutomotivo):
    def obter_descricao(self): return "Reparo de Suspensão"
    def obter_custo(self): return 800.00

# Padrão 2: Factory Method
class ServicoFactory:
    @staticmethod
    def criar_servico(tipo: str) -> ServicoAutomotivo:
        if tipo == "motor": return ReparoMotor()
        if tipo == "suspensao": return ReparoSuspensao()
        raise ValueError("Serviço não encontrado.")

# Padrão 3: Decorator
class ServicoDecorator(ServicoAutomotivo):
    def __init__(self, servico: ServicoAutomotivo):
        self._servico = servico
    def obter_descricao(self): return self._servico.obter_descricao()
    def obter_custo(self): return self._servico.obter_custo()

class TrocaOleo(ServicoDecorator):
    def obter_descricao(self): return self._servico.obter_descricao() + " + Troca de Óleo"
    def obter_custo(self): return self._servico.obter_custo() + 180.00

class Lavagem(ServicoDecorator):
    def obter_descricao(self): return self._servico.obter_descricao() + " + Lavagem"
    def obter_custo(self): return self._servico.obter_custo() + 70.00

# Padrão 4: Observer
class Observador(ABC):
    @abstractmethod
    def atualizar(self, status: str): pass

class ClienteAPI(Observador):
    def __init__(self, nome: str):
        self.nome = nome
        self.historico_mensagens = []

    def atualizar(self, status: str):
        self.historico_mensagens.append(f"Notificação para {self.nome}: Veículo {status}")

class OrdemDeServico:
    def __init__(self, servico: ServicoAutomotivo):
        self.servico = servico
        self._observadores = []

    def adicionar_observador(self, obs: Observador):
        self._observadores.append(obs)

    def alterar_status(self, novo_status: str):
        for obs in self._observadores:
            obs.atualizar(novo_status)

# Schemas de Request
class PedidoServico(BaseModel):
    nome_cliente: str
    veiculo: str
    servico_base: str
    adicionais: List[str]

# Endpoints
@app.get("/api/info")
def get_info():
    config = ConfiguracaoOficina()
    return {"oficina": config.nome}

@app.post("/api/ordem-servico")
def criar_ordem(pedido: PedidoServico):
    servico = ServicoFactory.criar_servico(pedido.servico_base)

    if "oleo" in pedido.adicionais:
        servico = TrocaOleo(servico)
    if "lavagem" in pedido.adicionais:
        servico = Lavagem(servico)

    cliente = ClienteAPI(pedido.nome_cliente)
    os = OrdemDeServico(servico)
    os.adicionar_observador(cliente)

    os.alterar_status("em análise no pátio.")
    os.alterar_status("pronto para retirada!")

    return {
        "cliente": pedido.nome_cliente,
        "veiculo": pedido.veiculo,
        "servico_realizado": servico.obter_descricao(),
        "total_pagar": servico.obter_custo(),
        "notificacoes_enviadas": cliente.historico_mensagens
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)