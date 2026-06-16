"""
Módulo de Entidades de Domínio — Camada mais interna da Clean Architecture.

SOLID aplicado:
- SRP: Cada classe tem uma única responsabilidade (Configuração, Interface, Serviço específico).
- OCP: ServicoAutomotivo é uma abstração aberta para extensão (novos serviços)
       sem modificar o código existente.
- LSP: Qualquer subclasse de ServicoAutomotivo pode substituir a classe base sem quebrar o sistema.
- ISP: A interface ServicoAutomotivo expõe apenas os métodos essenciais.
- DIP: Código externo depende de ServicoAutomotivo (abstração), não de ReparoMotor (concreção).

Clean Code aplicado:
- Nomes expressivos e autodocumentáveis (ServicoAutomotivo, obter_descricao, obter_custo).
- Sem números mágicos: valores encapsulados em cada classe concreta.
- Funções pequenas com responsabilidade única.
"""

from abc import ABC, abstractmethod


# ──────────────────────────────────────────────
# PADRÃO 1: SINGLETON
# Garante uma única instância da configuração global da aplicação.
# Útil para centralizar dados que não devem ser duplicados (nome da empresa, config de ambiente).
# ──────────────────────────────────────────────
class ConfiguracaoOficina:
    """
    Configuração global da oficina.

    Implementa o padrão Singleton para garantir que toda a aplicação
    compartilhe a mesma instância de configuração — evitando inconsistências.
    """

    _instancia = None

    def __new__(cls):
        """Cria a instância apenas na primeira chamada; reutiliza nas demais."""
        if cls._instancia is None:
            cls._instancia = super(ConfiguracaoOficina, cls).__new__(cls)
            cls._instancia.nome = "Auto Mecânica Central - Microsserviços"
        return cls._instancia


# ──────────────────────────────────────────────
# CAMADA DE ENTIDADES — Enterprise Business Rules
# Interfaces puras que definem o contrato dos serviços automotivos.
# Nenhuma dependência de framework externo nesta camada.
# ──────────────────────────────────────────────
class ServicoAutomotivo(ABC):
    """
    Interface base para todos os serviços automotivos.

    Princípio SOLID aplicado — OCP: aberta para extensão (novas classes concretas
    como 'ReparoFreios', 'TrocaPneu') sem modificar esta interface.
    Todos os Decorators também herdam desta classe, permitindo composição dinâmica.
    """

    @abstractmethod
    def obter_descricao(self) -> str:
        """Retorna a descrição legível do serviço."""
        pass

    @abstractmethod
    def obter_custo(self) -> float:
        """Retorna o custo total do serviço em reais (BRL)."""
        pass


class ReparoMotor(ServicoAutomotivo):
    """
    Serviço concreto: Reparo de Motor.

    Princípio LSP: substitui ServicoAutomotivo sem alterar o comportamento esperado.
    """

    CUSTO_BASE: float = 1500.00
    DESCRICAO: str = "Reparo de Motor"

    def obter_descricao(self) -> str:
        return self.DESCRICAO

    def obter_custo(self) -> float:
        return self.CUSTO_BASE


class ReparoSuspensao(ServicoAutomotivo):
    """
    Serviço concreto: Reparo de Suspensão.

    Princípio LSP: substitui ServicoAutomotivo sem alterar o comportamento esperado.
    """

    CUSTO_BASE: float = 800.00
    DESCRICAO: str = "Reparo de Suspensão"

    def obter_descricao(self) -> str:
        return self.DESCRICAO

    def obter_custo(self) -> float:
        return self.CUSTO_BASE
