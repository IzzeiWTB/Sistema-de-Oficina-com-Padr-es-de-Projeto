from abc import ABC, abstractmethod

class Observador(ABC):
    @abstractmethod
    def atualizar(self, status: str):
        pass

class OrdemDeServico:
    def __init__(self):
        self._observadores = []

    def adicionar_observador(self, obs: Observador):
        self._observadores.append(obs)

    def alterar_status(self, novo_status: str):
        for obs in self._observadores:
            obs.atualizar(novo_status)
