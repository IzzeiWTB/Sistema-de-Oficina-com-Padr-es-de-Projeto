# encoding: utf-8
Feature: Calcular Custo de Ordem de Servico
  Para fornecer orcamentos precisos e transparentes aos clientes
  Como atendente da oficina
  Eu quero que o sistema calcule o valor total incluindo servicos adicionais de forma correta

  Scenario: Reparo de motor simples, sem adicionais
    Given que um cliente solicita o servico de "motor"
    Then o valor total a pagar deve ser 1500.00
    And a descricao deve conter "Reparo de Motor"

  Scenario: Adicionar troca de oleo ao reparo de motor
    Given que um cliente solicita o servico de "motor"
    When ele adiciona o extra de "oleo"
    Then o valor total a pagar deve ser 1680.00
    And a descricao deve conter "Troca de Oleo"

  Scenario: Reparo de motor com troca de oleo e lavagem
    Given que um cliente solicita o servico de "motor"
    When ele adiciona o extra de "oleo"
    And ele adiciona o extra de "lavagem"
    Then o valor total a pagar deve ser 1750.00

  Scenario: Reparo de suspensao com lavagem
    Given que um cliente solicita o servico de "suspensao"
    When ele adiciona o extra de "lavagem"
    Then o valor total a pagar deve ser 870.00

  Scenario: Servico invalido deve gerar erro
    Given que um cliente solicita o servico de "motor_a_jato"
    Then o sistema deve retornar um erro de servico nao encontrado
