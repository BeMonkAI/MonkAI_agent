# Exemplos de Definição de Agentes

Esta pasta contém exemplos práticos de como definir e implementar agentes usando o framework MonkAI Agent. Os exemplos demonstram diferentes tipos de agentes e suas funcionalidades.

## 📋 Conteúdo

- [Agent Definition (Jupyter Notebook)](#agent-definition-jupyter-notebook)
- [Analista de Negócios](#analista-de-negócios)
- [Como Executar](#como-executar)
- [Pré-requisitos](#pré-requisitos)

## 📊 Agent Definition (Jupyter Notebook)

**Arquivo:** `agent_definition.ipynb`

Este notebook demonstra a criação de um **Calculator Agent** - um agente especializado em operações matemáticas complexas.

### Funcionalidades do Calculator Agent

O agente possui três funções matemáticas principais:

1. **`my_function(a: float, b: float)`**
   - Realiza múltiplas operações matemáticas em uma única expressão
   - Retorna: (divisão, multiplicação, sequência de números, valor máximo)
   - Exemplo: `my_function(10, 2)` → `(5.0, 20, [10, 11, ...], valor_calculado)`

2. **`fibonacci(num1: str)`**
   - Calcula a sequência de Fibonacci
   - Parâmetro: número de elementos da sequência
   - Retorna: lista com a sequência de Fibonacci

3. **`bernoulli(n: int)`**
   - Calcula os primeiros n números de Bernoulli
   - Parâmetro: quantidade de números de Bernoulli a calcular
   - Retorna: lista com os números de Bernoulli

### Exemplo de Uso

```python
from monkai_agent.types import Agent

calculator_agent = Agent(
    name="Calculator Agent",
    instructions="""You are an agent responsible for performing mathematical calculations.
                You have access to mathematical functions for complex calculations.""",
    functions=[my_function, fibonacci, bernoulli]
)

# Executar em modo interativo
await run_simples_demo_loop(calculator_agent, api_key="sua_api_key")
```

## 💼 Analista de Negócios

**Arquivo:** `analista_negocio_agente_monkai.py`

Este exemplo demonstra a criação de um agente especializado em análise de negócios e insights financeiros.

### Características do Agente

- **Nome:** "Agente Analista de Negócios"
- **Especialização:** Interpretação de tendências de mercado e análise financeira
- **Funcionalidades:**
  - Resumir relatórios financeiros e de mercado
  - Destacar indicadores financeiros relevantes (KPIs)
  - Sugerir decisões estratégicas baseadas em dados
  - Identificar riscos, oportunidades e tendências emergentes

### Exemplo de Uso

```python
from monkai_agent import Agent, AgentManager

# Configurar o gerenciador
manager = AgentManager(api_key="sua_api_key")

# Criar o agente
agente = Agent(
    name="Agente Analista de Negócios",
    instructions="""Você é um Analista de Negócios experiente..."""
)

# Executar consulta
result = asyncio.run(manager.run(
    "Resuma os principais insights financeiros dos relatórios econômicos desta semana.",
    agent=agente
))
```

### Estilo de Resposta

O agente foi configurado para:
- ✅ Usar bullet points sempre que possível
- ✅ Evitar jargões técnicos
- ✅ Ser direto e claro
- ✅ Focar em recomendações práticas

## 🚀 Como Executar

### Notebook (agent_definition.ipynb)

1. Abra o Jupyter Notebook
2. Execute as células sequencialmente
3. Na última célula, substitua `"api_key"` pela sua chave de API real
4. Execute o loop interativo para testar o agente

### Script Python (analista_negocio_agente_monkai.py)

1. Substitua a `api_key` no código pela sua chave real
2. Execute o script:
   ```bash
   python analista_negocio_agente_monkai.py
   ```

## 📋 Pré-requisitos

### Instalação

```bash
pip install monkai_agent
```

### Dependências

- Python 3.8+
- monkai_agent
- asyncio (incluído no Python padrão)

### Configuração

1. **API Key:** Ambos os exemplos requerem uma chave de API válida
2. **Ambiente:** Recomenda-se usar um ambiente virtual Python

```bash
# Ativar ambiente virtual (se usando .venv)
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

## 📝 Estrutura do Agente

Ambos os exemplos seguem a estrutura padrão do MonkAI Agent:

```python
Agent(
    name="Nome do Agente",           # Nome identificador
    instructions="Instruções...",    # Prompt/contexto do agente
    functions=[func1, func2]         # Funções disponíveis (opcional)
)
```

## 🔧 Personalização

Você pode modificar estes exemplos para:

- Adicionar novas funções aos agentes
- Alterar as instruções para diferentes especialidades
- Integrar com diferentes provedores de LLM
- Implementar funcionalidades customizadas

## 📚 Próximos Passos

Após executar estes exemplos, explore:

- `../triage/` - Exemplos de agentes em sistema de triagem
- `../mcp_example/` - Integração com Model Context Protocol
- `../creators_and_manager/` - Criação avançada de agentes

---

*Para mais informações, consulte a documentação principal do MonkAI Agent.*
