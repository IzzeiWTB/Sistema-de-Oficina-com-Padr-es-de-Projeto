import requests
import os
from domain.observer import Observador

class ServicoNotificacaoAdapter(Observador):
    """
    Adapter que implementa o padrão Observer comunicando-se
    com outro microsserviço via HTTP.
    """
    def __init__(self, nome_cliente: str):
        self.nome_cliente = nome_cliente
        self.notificacao_url = os.getenv("NOTIFICACAO_URL", "http://localhost:8002")

    def atualizar(self, status: str):
        try:
            payload = {
                "cliente": self.nome_cliente,
                "mensagem": f"Veículo {status}"
            }
            requests.post(f"{self.notificacao_url}/api/notificar", json=payload, timeout=2)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao notificar microsserviço: {e}")
