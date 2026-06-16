"""
Módulo do Caso de Uso: Criar Ordem de Serviço.

Camada de Use Cases da Clean Architecture — orquestra as regras de aplicação.

SOLID aplicado:
- SRP: Esta classe tem uma única responsabilidade — coordenar o fluxo de
       criação de uma ordem de serviço. Não cuida de HTTP, banco de dados, nem de UI.
- DIP: Depende da abstração ServicoAutomotivo (via Factory), não das implementações concretas.
       O Observer (ServicoNotificacaoAdapter) também é injetado como abstração Observador.

Clean Code:
- Nome do método 'executar' comunica claramente a intenção.
- Fluxo linear e sem efeitos colaterais inesperados.
- Comentários explicam o *porquê*, não o *o quê*.
"""

from typing import List, Dict, Any

from domain.patterns import ServicoFactory, TrocaOleo, Lavagem
from domain.observer import OrdemDeServico
from adapters.api.notificacao_adapter import ServicoNotificacaoAdapter


class CriarOrdemServicoUseCase:
    """
    Caso de Uso: Criar uma nova Ordem de Serviço.

    Orquestra o fluxo completo:
    1. Cria o serviço base via Factory Method.
    2. Aplica os serviços adicionais via Decorator.
    3. Configura o Observer para notificações automáticas.
    4. Dispara as mudanças de status, acionando as notificações.
    5. Retorna o resultado final consolidado.
    """

    def executar(
        self,
        nome_cliente: str,
        veiculo: str,
        servico_base: str,
        adicionais: List[str],
    ) -> Dict[str, Any]:
        """
        Executa a criação de uma ordem de serviço.

        Args:
            nome_cliente: Nome completo do cliente.
            veiculo: Identificação do veículo (modelo/placa).
            servico_base: Tipo do serviço principal ('motor' ou 'suspensao').
            adicionais: Lista de serviços adicionais ('oleo', 'lavagem').

        Returns:
            Dicionário com os dados consolidados da ordem:
            cliente, veiculo, servico_realizado, total_pagar.

        Raises:
            ValueError: Se o servico_base não for reconhecido pela Factory.
        """
        # PADRÃO Factory Method: cria o serviço base sem acoplar ao tipo concreto
        servico = ServicoFactory.criar_servico(servico_base)

        # PADRÃO Decorator: envolve o serviço base com adicionais de forma dinâmica
        # Ordem importa: cada Decorator encapsula o anterior, formando uma cadeia
        if "oleo" in adicionais:
            servico = TrocaOleo(servico)
        if "lavagem" in adicionais:
            servico = Lavagem(servico)

        # PADRÃO Observer: registra o adapter que irá disparar HTTP para o Microsserviço 2
        # O OrdemDeServico não sabe *como* a notificação é enviada — apenas que deve ser enviada
        cliente_observer = ServicoNotificacaoAdapter(nome_cliente)
        ordem = OrdemDeServico()
        ordem.adicionar_observador(cliente_observer)

        # Disparar eventos de status — cada chamada notifica todos os observadores registrados
        ordem.alterar_status("em análise no pátio.")
        ordem.alterar_status("pronto para retirada!")

        return {
            "cliente": nome_cliente,
            "veiculo": veiculo,
            "servico_realizado": servico.obter_descricao(),
            "total_pagar": servico.obter_custo(),
        }
