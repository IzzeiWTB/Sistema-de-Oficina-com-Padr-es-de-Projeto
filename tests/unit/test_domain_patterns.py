"""
Testes Unitários — Camada de Domínio (TDD).

Estes testes foram escritos seguindo a metodologia TDD (Test-Driven Development):
os comportamentos esperados são definidos aqui antes (ou em conjunto) com a
implementação, garantindo que o domínio funcione de forma isolada — sem
dependência de framework web, banco de dados ou rede.

Padrões testados:
- Singleton (ConfiguracaoOficina)
- Factory Method (ServicoFactory)
- Decorator (TrocaOleo, Lavagem)
"""

import sys
import os

# Garante que o módulo do servico_oficina esteja no path de importação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../servico_oficina")))

import pytest
from domain.entities import ConfiguracaoOficina, ReparoMotor, ReparoSuspensao
from domain.patterns import ServicoFactory, TrocaOleo, Lavagem


# ── SINGLETON ──────────────────────────────────────────────────────────
class TestSingleton:
    def test_mesma_instancia_em_chamadas_diferentes(self):
        """Garante que ConfiguracaoOficina retorna sempre o mesmo objeto."""
        config1 = ConfiguracaoOficina()
        config2 = ConfiguracaoOficina()
        assert config1 is config2, "Singleton falhou: instâncias diferentes foram criadas."

    def test_nome_da_oficina_correto(self):
        """Verifica que a configuração contém o nome esperado da oficina."""
        config = ConfiguracaoOficina()
        assert "Auto Mecânica Central" in config.nome


# ── FACTORY METHOD ─────────────────────────────────────────────────────
class TestFactoryMethod:
    def test_factory_cria_reparo_motor(self):
        """Deve instanciar ReparoMotor quando o tipo 'motor' for solicitado."""
        servico = ServicoFactory.criar_servico("motor")
        assert isinstance(servico, ReparoMotor)

    def test_factory_cria_reparo_suspensao(self):
        """Deve instanciar ReparoSuspensao quando o tipo 'suspensao' for solicitado."""
        servico = ServicoFactory.criar_servico("suspensao")
        assert isinstance(servico, ReparoSuspensao)

    def test_custo_motor_correto(self):
        """O custo base do reparo de motor deve ser R$ 1.500,00."""
        servico = ServicoFactory.criar_servico("motor")
        assert servico.obter_custo() == 1500.00

    def test_custo_suspensao_correto(self):
        """O custo base do reparo de suspensão deve ser R$ 800,00."""
        servico = ServicoFactory.criar_servico("suspensao")
        assert servico.obter_custo() == 800.00

    def test_factory_levanta_erro_para_servico_invalido(self):
        """Deve levantar ValueError para um tipo de serviço não cadastrado."""
        with pytest.raises(ValueError, match="não encontrado"):
            ServicoFactory.criar_servico("voar")


# ── DECORATOR ──────────────────────────────────────────────────────────
class TestDecorator:
    def test_troca_oleo_adiciona_custo_correto(self):
        """TrocaOleo deve somar R$ 180,00 ao custo do serviço base."""
        servico = ServicoFactory.criar_servico("motor")
        servico_com_oleo = TrocaOleo(servico)
        assert servico_com_oleo.obter_custo() == 1500.00 + 180.00

    def test_troca_oleo_adiciona_descricao(self):
        """TrocaOleo deve incluir 'Troca de Óleo' na descrição final."""
        servico = TrocaOleo(ServicoFactory.criar_servico("motor"))
        assert "Troca de Óleo" in servico.obter_descricao()

    def test_lavagem_adiciona_custo_correto(self):
        """Lavagem deve somar R$ 70,00 ao custo do serviço base."""
        servico = Lavagem(ServicoFactory.criar_servico("motor"))
        assert servico.obter_custo() == 1500.00 + 70.00

    def test_decorators_encadeados_acumulam_custos(self):
        """Dois Decorators encadeados devem acumular corretamente os custos."""
        servico = ServicoFactory.criar_servico("suspensao")
        servico = TrocaOleo(servico)
        servico = Lavagem(servico)
        custo_esperado = 800.00 + 180.00 + 70.00
        assert servico.obter_custo() == custo_esperado

    def test_decorators_encadeados_acumulam_descricao(self):
        """A descrição final deve conter todos os serviços adicionados."""
        servico = Lavagem(TrocaOleo(ServicoFactory.criar_servico("motor")))
        descricao = servico.obter_descricao()
        assert "Reparo de Motor" in descricao
        assert "Troca de Óleo" in descricao
        assert "Lavagem" in descricao

    def test_decorator_nao_altera_servico_base_original(self):
        """O serviço base não deve ser modificado ao aplicar um Decorator."""
        base = ServicoFactory.criar_servico("motor")
        _ = TrocaOleo(base)
        assert base.obter_custo() == 1500.00, "Decorator alterou o serviço base indevidamente."
