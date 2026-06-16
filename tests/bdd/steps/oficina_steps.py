import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../servico_oficina")))

from behave import given, when, then
from domain.patterns import ServicoFactory, TrocaOleo, Lavagem


@given('que um cliente solicita o servico de "{servico_base}"')
def step_solicitar_servico(context, servico_base):
    context.erro = None
    try:
        context.servico = ServicoFactory.criar_servico(servico_base)
    except ValueError as e:
        context.servico = None
        context.erro = e


@when('ele adiciona o extra de "oleo"')
def step_adicionar_oleo(context):
    if context.servico:
        context.servico = TrocaOleo(context.servico)


@when('ele adiciona o extra de "lavagem"')
def step_adicionar_lavagem(context):
    if context.servico:
        context.servico = Lavagem(context.servico)


@then("o valor total a pagar deve ser {valor:f}")
def step_verificar_valor(context, valor):
    assert context.servico is not None, "Servico nao foi criado."
    custo = context.servico.obter_custo()
    assert custo == valor, f"Esperado R$ {valor:.2f}, mas calculado R$ {custo:.2f}"


@then('a descricao deve conter "{trecho}"')
def step_verificar_descricao(context, trecho):
    assert context.servico is not None
    import unicodedata
    def normalizar(texto):
        return unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode("ascii").lower()
    descricao_norm = normalizar(context.servico.obter_descricao())
    trecho_norm = normalizar(trecho)
    assert trecho_norm in descricao_norm, \
        f"Esperado '{trecho}' na descricao, mas obteve: '{context.servico.obter_descricao()}'"



@then("o sistema deve retornar um erro de servico nao encontrado")
def step_verificar_erro(context):
    assert context.erro is not None, "Era esperado um erro, mas nenhum ocorreu."
    assert isinstance(context.erro, ValueError)
