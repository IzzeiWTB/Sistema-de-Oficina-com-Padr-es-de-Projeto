"""
Módulo de Padrões de Projeto (Design Patterns) — Camada de Domínio.

Contém a implementação dos padrões Factory Method e Decorator,
aplicados ao contexto de criação e composição de serviços automotivos.

Clean Code aplicado:
- Nomes revelam a intenção: ServicoFactory (cria), TrocaOleo (decora com óleo).
- Cada classe tem uma única responsabilidade.
- Sem duplicação: o Decorator reutiliza o comportamento do serviço base via composição.
"""

from domain.entities import ServicoAutomotivo, ReparoMotor, ReparoSuspensao


# ──────────────────────────────────────────────
# PADRÃO 2: FACTORY METHOD
# Encapsula a lógica de instanciação de ServicoAutomotivo.
# O Use Case não precisa saber *como* o objeto é criado — apenas qual tipo quer.
# Princípio DIP: o Use Case depende da abstração ServicoAutomotivo,
# não das implementações concretas ReparoMotor / ReparoSuspensao.
# ──────────────────────────────────────────────
class ServicoFactory:
    """
    Fábrica de serviços automotivos.

    Implementa o padrão Factory Method para centralizar a criação de instâncias
    de ServicoAutomotivo. Para adicionar um novo serviço (ex: TrocaPneu),
    basta criar a classe e registrá-la aqui — o restante do sistema não precisa mudar.
    Isso atende ao princípio OCP (Open/Closed).
    """

    @staticmethod
    def criar_servico(tipo: str) -> ServicoAutomotivo:
        """
        Cria e retorna a instância do serviço correspondente ao tipo informado.

        Args:
            tipo: Identificador do serviço. Valores aceitos: 'motor', 'suspensao'.

        Returns:
            Instância concreta de ServicoAutomotivo.

        Raises:
            ValueError: Se o tipo de serviço não for reconhecido.
        """
        catalogo = {
            "motor": ReparoMotor,
            "suspensao": ReparoSuspensao,
        }
        if tipo not in catalogo:
            raise ValueError(f"Serviço '{tipo}' não encontrado. Disponíveis: {list(catalogo.keys())}")
        return catalogo[tipo]()


# ──────────────────────────────────────────────
# PADRÃO 3: DECORATOR
# Adiciona responsabilidades extras (Óleo, Lavagem) a um ServicoAutomotivo
# de forma dinâmica, sem criar explosão de subclasses.
# Ex: em vez de criar ReparoMotorComOleo, ReparoMotorComLavagem, ReparoMotorComOleoELavagem...
# simplesmente envolve o serviço base com Decorators encadeáveis.
# Princípio OCP: estende o comportamento sem modificar as classes existentes.
# ──────────────────────────────────────────────
class ServicoDecorator(ServicoAutomotivo):
    """
    Decorador base para serviços automotivos.

    Encapsula um ServicoAutomotivo e delega as chamadas para ele por padrão.
    Subclasses sobrescrevem os métodos para adicionar comportamento extra.
    Isso permite encadeamento: TrocaOleo(Lavagem(ReparoMotor())).
    """

    def __init__(self, servico: ServicoAutomotivo):
        """
        Args:
            servico: O serviço a ser decorado (pode ser base ou outro decorator).
        """
        self._servico = servico

    def obter_descricao(self) -> str:
        """Delega para o serviço encapsulado."""
        return self._servico.obter_descricao()

    def obter_custo(self) -> float:
        """Delega para o serviço encapsulado."""
        return self._servico.obter_custo()


class TrocaOleo(ServicoDecorator):
    """
    Adiciona o serviço de Troca de Óleo a qualquer ServicoAutomotivo.
    Custo adicional: R$ 180,00.
    """

    CUSTO_ADICIONAL: float = 180.00
    DESCRICAO_ADICIONAL: str = " + Troca de Óleo"

    def obter_descricao(self) -> str:
        return super().obter_descricao() + self.DESCRICAO_ADICIONAL

    def obter_custo(self) -> float:
        return super().obter_custo() + self.CUSTO_ADICIONAL


class Lavagem(ServicoDecorator):
    """
    Adiciona o serviço de Lavagem Completa a qualquer ServicoAutomotivo.
    Custo adicional: R$ 70,00.
    """

    CUSTO_ADICIONAL: float = 70.00
    DESCRICAO_ADICIONAL: str = " + Lavagem"

    def obter_descricao(self) -> str:
        return super().obter_descricao() + self.DESCRICAO_ADICIONAL

    def obter_custo(self) -> float:
        return super().obter_custo() + self.CUSTO_ADICIONAL
