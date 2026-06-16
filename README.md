# 🔧 Sistema de Gestão de Ordens de Serviço — Auto Mecânica Central

> **Prova de Engenharia de Software** — Demonstração prática de Clean Code, SOLID, Design Patterns, TDD, BDD, Arquitetura Limpa, Microsserviços e Docker.

---

## 📋 Descrição do Problema

Oficinas mecânicas tradicionais enfrentam dificuldades em gerenciar ordens de serviço de forma organizada: serviços são combinados manualmente, clientes não recebem atualizações sobre o status do veículo e não há separação de responsabilidades entre o núcleo de negócio e a infraestrutura de comunicação.

**Solução proposta:** Um sistema de software com arquitetura orientada a microsserviços que:
- Calcula orçamentos dinamicamente com base no tipo de serviço e adicionais selecionados
- Notifica automaticamente o cliente a cada mudança de status da ordem de serviço
- Separa de forma clara o núcleo de negócio da infraestrutura (APIs, banco de dados, serviços externos)

---

## 🏗️ Arquitetura Geral

```
┌─────────────────────────────────────────────────────────┐
│                     CLIENTE (Browser)                   │
│                  frontend/index.html                    │
└───────────────────┬─────────────────┬───────────────────┘
                    │                 │  polling a cada 4s
          POST /api/ordem-servico   GET /api/historico
                    │                 │
         ┌──────────▼──────┐   ┌──────▼──────────────┐
         │  Microsserviço  │   │  Microsserviço       │
         │     Oficina     │──►│   Notificações       │
         │   Porta 8001    │   │    Porta 8002        │
         └─────────────────┘   └─────────────────────┘
           (Factory, Decorator,    (Observer Pattern)
            Singleton, Clean Arch)
```

---

## 📁 Estrutura do Projeto (Arquitetura Limpa)

```
Projeto Oficina/
├── docker-compose.yml              # Orquestração dos microsserviços
├── render.yaml                     # Deploy em nuvem (Render.com)
├── frontend/
│   └── index.html                  # Interface Web
├── servico_oficina/                # Microsserviço 1 — Porta 8001
│   ├── Dockerfile
│   ├── main.py                     # Camada de Frameworks (FastAPI)
│   ├── adapters/
│   │   └── api/
│   │       └── notificacao_adapter.py  # Interface com Serviço externo
│   ├── domain/                     # Camada de Entidades (Regras de Negócio)
│   │   ├── entities.py             # Singleton + Interfaces ABC
│   │   ├── patterns.py             # Factory Method + Decorator
│   │   └── observer.py             # Observer Pattern
│   └── use_cases/                  # Camada de Casos de Uso
│       └── criar_ordem_servico.py  # Orquestração do fluxo principal
├── servico_notificacao/            # Microsserviço 2 — Porta 8002
│   ├── Dockerfile
│   └── main.py                     # API de recebimento de eventos
└── tests/
    ├── unit/
    │   └── test_domain_patterns.py # Testes unitários (TDD)
    └── bdd/
        ├── features/
        │   └── oficina.feature     # Cenários Gherkin (BDD)
        └── steps/
            └── oficina_steps.py    # Implementação dos steps
```

### Camadas da Clean Architecture

| Camada | Pasta | Responsabilidade |
|--------|-------|-----------------|
| **Entities** | `domain/entities.py` | Regras de negócio fundamentais, sem dependências externas |
| **Use Cases** | `use_cases/` | Orquestração do fluxo de negócio |
| **Interface Adapters** | `adapters/` | Traduz dados entre Use Cases e serviços externos |
| **Frameworks & Drivers** | `main.py` | FastAPI, HTTP, I/O |

> ✅ **Regra de Dependência**: as camadas internas (`domain`, `use_cases`) **nunca** importam das camadas externas. O `main.py` depende dos Use Cases, que dependem do Domain — nunca o contrário.

---

## 🎨 Design Patterns Aplicados

### 1. Singleton — `ConfiguracaoOficina`
**Problema resolvido:** garantir que existe apenas uma instância da configuração global da aplicação.

```python
class ConfiguracaoOficina:
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.nome = "Auto Mecânica Central"
        return cls._instancia
```

### 2. Factory Method — `ServicoFactory`
**Problema resolvido:** desacoplar a criação de objetos `ServicoAutomotivo` do código que os usa. Para adicionar um novo serviço (ex: Alinhamento), basta criar a classe e registrar na factory — sem alterar o Use Case.

```python
class ServicoFactory:
    @staticmethod
    def criar_servico(tipo: str) -> ServicoAutomotivo:
        if tipo == "motor": return ReparoMotor()
        if tipo == "suspensao": return ReparoSuspensao()
        raise ValueError("Serviço não encontrado.")
```

### 3. Decorator — `TrocaOleo`, `Lavagem`
**Problema resolvido:** adicionar serviços extras (Troca de Óleo, Lavagem) a qualquer serviço base de forma dinâmica, sem criar combinações estáticas de classes (ex: `ReparoMotorComOleo`, `ReparoMotorComLavagem`...).

```python
class TrocaOleo(ServicoDecorator):
    def obter_custo(self) -> float:
        return super().obter_custo() + 180.00  # Adiciona ao custo base
```

### 4. Observer — `OrdemDeServico` + `ServicoNotificacaoAdapter`
**Problema resolvido:** notificar automaticamente os clientes ao mudar o status da ordem, sem acoplar a lógica de negócio ao mecanismo de notificação. O `OrdemDeServico` não sabe como a notificação é enviada — apenas dispara o evento.

```python
os = OrdemDeServico()
os.adicionar_observador(ServicoNotificacaoAdapter(nome_cliente))
os.alterar_status("pronto para retirada!")  # Dispara HTTP para Microsserviço 2
```

---

## 🧱 Princípios SOLID

| Princípio | Onde é aplicado | Como |
|-----------|----------------|------|
| **S** — Single Responsibility | `CriarOrdemServicoUseCase` | Responsável apenas por orquestrar a criação da ordem; não cuida de HTTP nem de persistência |
| **O** — Open/Closed | `ServicoAutomotivo` + `ServicoDecorator` | Aberto para extensão (novos serviços/adicionais) sem modificar o código existente |
| **L** — Liskov Substitution | `TrocaOleo`, `Lavagem`, `ReparoMotor` | Qualquer subclasse de `ServicoAutomotivo` pode substituir a base sem quebrar o sistema |
| **I** — Interface Segregation | `ServicoAutomotivo` (ABC) com apenas 2 métodos | Interfaces pequenas e focadas; as classes implementam apenas o que precisam |
| **D** — Dependency Inversion | `CriarOrdemServicoUseCase` depende da abstração `ServicoAutomotivo`, não de `ReparoMotor` | O Use Case recebe a abstração via Factory, não a implementação concreta |

---

## 🧪 Testes — TDD e BDD

### TDD com Pytest
Os testes unitários foram escritos para verificar cada padrão de forma isolada, sem dependência de framework web:

```bash
python -m pytest tests/unit/ -v
```

Testes existentes:
- `test_singleton_configuracao` — garante que apenas 1 instância existe
- `test_factory_method_motor` — verifica criação via Factory
- `test_factory_method_servico_invalido` — verifica tratamento de erro
- `test_decorator_troca_oleo` — verifica composição de custo
- `test_decorator_multiplos` — verifica encadeamento de Decorators

### BDD com Behave
Cenários escritos em linguagem natural (Gherkin), verificando o comportamento de ponta a ponta do domínio:

```bash
python -m behave tests/bdd/
```

```gherkin
Scenario: Adicionar reparo de motor com troca de óleo e lavagem
  Given que um cliente solicita o serviço de "motor"
  When ele adiciona o extra de "oleo"
  And ele adiciona o extra de "lavagem"
  Then o valor total a pagar deve ser 1750.00
```

---

## 🐳 Docker e Docker Compose

Cada microsserviço possui seu próprio `Dockerfile`. O `docker-compose.yml` os orquestra em uma rede isolada, onde o Serviço de Oficina consegue se comunicar com o Serviço de Notificações pelo nome do container.

```bash
# Subir todos os serviços
docker-compose up --build -d

# Ver logs em tempo real
docker-compose logs -f

# Parar tudo
docker-compose down
```

| Container | Imagem | Porta |
|-----------|--------|-------|
| `servico_oficina` | python:3.10-slim | 8001 |
| `servico_notificacao` | python:3.10-slim | 8002 |

---

## 🚀 Como Executar Localmente (sem Docker)

```bash
# Terminal 1 — Microsserviço Notificações
cd servico_notificacao
pip install -r requirements.txt
uvicorn main:app --port 8002

# Terminal 2 — Microsserviço Oficina
cd servico_oficina
pip install -r requirements.txt
uvicorn main:app --port 8001

# Abrir o frontend
# Abra frontend/index.html no navegador
```

Documentação automática das APIs:
- Oficina: http://localhost:8001/docs
- Notificações: http://localhost:8002/docs

---

## ☁️ Deploy em Nuvem (Render.com)

O arquivo `render.yaml` configura o deploy automático de ambos os microsserviços no Render.com como _Web Services_ independentes.

**URL da aplicação publicada:** `(link a ser inserido após o deploy)`

---

## 🔍 Evidências de Clean Code

1. **Nomes expressivos:** `CriarOrdemServicoUseCase`, `ServicoNotificacaoAdapter`, `obter_custo()` — nenhuma abreviação críptica
2. **Funções com responsabilidade única:** cada método faz exatamente uma coisa
3. **Docstrings em todas as classes e métodos públicos** explicando propósito e padrão utilizado
4. **Sem números mágicos:** custos dos serviços encapsulados dentro das próprias classes de domínio
5. **Separação de camadas:** nenhum import de `fastapi` dentro do `domain/`

---

## ⚙️ Justificativa das Escolhas Técnicas

| Escolha | Justificativa |
|---------|--------------|
| **FastAPI** | Alta performance, tipagem nativa com Pydantic, documentação Swagger automática |
| **Python** | Simplicidade e expressividade para demonstrar padrões de forma clara |
| **Docker Compose** | Permite replicar o ambiente em qualquer máquina com um único comando |
| **Render.com** | Plataforma gratuita com suporte nativo a Python, deploy via Git e HTTPS automático |
| **Behave (BDD)** | Sintaxe Gherkin legível por não-técnicos, ideal para documentar comportamentos de negócio |
| **Pytest (TDD)** | Framework padrão Python, fixtures poderosas, integração com CI/CD |
| **2 Microsserviços** | Separação de responsabilidades: o domínio de "ordens" é independente do domínio de "notificações"; escalam de forma independente |
