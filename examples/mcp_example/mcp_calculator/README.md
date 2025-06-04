# Calculator MCP Agent Example

Este exemplo demonstra como criar um `MCPAgent` que se conecta ao servidor Calculator MCP para acessar ferramentas de cálculo matemático.

## Arquivos

- `calculator_mcp_server.py` - Servidor MCP que fornece ferramentas de calculadora básicas
- `calculator_agent_creator.py` - Creator que retorna um MCPAgent configurado para conectar ao servidor Calculator
- `calculator_example.py` - Exemplo de uso do Calculator Agent
- `README.md` - Esta documentação

## Funcionalidades

O Calculator Agent fornece acesso às seguintes ferramentas através do servidor MCP:

### Ferramentas Disponíveis
- `add(a, b)` - Soma dois números
- `subtract(a, b)` - Subtrai dois números
- `multiply(a, b)` - Multiplica dois números
- `divide(a, b)` - Divide dois números (com proteção contra divisão por zero)

### Recursos Disponíveis
- `calculation://history` - Acesso ao histórico de cálculos

## Como Usar

### 1. Importar o CalculatorAgentCreator

```python
from calculator_agent_creator import CalculatorAgentCreator
```

### 2. Criar o Agent Creator

```python
creator = CalculatorAgentCreator(model="gpt-4")
```

### 3. Inicializar o Agent

```python
agent = await creator.initialize_agent()
```

### 4. Usar as Ferramentas de Cálculo

```python
# Realizar operações matemáticas
result = await agent.call_mcp_tool("add", {"a": 5, "b": 3})
print(f"5 + 3 = {result}")

result = await agent.call_mcp_tool("multiply", {"a": 4, "b": 7})
print(f"4 × 7 = {result}")
```

## Exemplo Completo

```python
import asyncio
from calculator_agent_creator import CalculatorAgentCreator

async def main():
    # Criar o agent creator
    creator = CalculatorAgentCreator(model="gpt-4")
    
    # Inicializar o agent e conectar ao servidor MCP
    agent = await creator.initialize_agent()
    
    # Verificar status da conexão
    status = agent.get_connection_status()
    print(f"Status da conexão: {status}")
    
    # Listar ferramentas disponíveis
    tools = agent.list_available_tools()
    print(f"Ferramentas disponíveis: {[tool.name for tool in tools]}")
    
    # Realizar cálculos
    result = await agent.call_mcp_tool("add", {"a": 10, "b": 20})
    print(f"10 + 20 = {result}")
    
    # Limpeza
    await agent.disconnect_all_clients()

# Executar o exemplo
asyncio.run(main())
```

## Executar o Exemplo

Para executar o exemplo completo:

```bash
# Ativar o ambiente virtual Python
source .venv/bin/activate

# Executar o exemplo
python calculator_example.py
```

## Características do CalculatorAgentCreator

### Parâmetros de Inicialização

- `model` (str): Modelo de linguagem a ser usado (padrão: "gpt-4")
- `server_script_path` (str, opcional): Caminho para o script do servidor. Se None, usa o caminho padrão
- `python_executable` (str): Executável Python para executar o servidor (padrão: "python")

### Métodos Principais

- `get_agent()` - Retorna o MCPAgent configurado
- `get_agent_briefing()` - Retorna uma descrição das capacidades do agent
- `initialize_agent()` - Inicializa o agent e estabelece conexões MCP
- `agent_name` - Propriedade que retorna o nome do agent

## Arquitetura

```
CalculatorAgentCreator
    ↓
MCPAgent (Calculator Agent)
    ↓
MCP Client Connection (stdio)
    ↓
Calculator MCP Server
    ↓
Ferramentas: add, subtract, multiply, divide
Recursos: calculation://history
```

## Tratamento de Erros

O agent possui tratamento robusto de erros:

- **Divisão por zero**: O servidor Calculator detecta e lança um erro apropriado
- **Conexão MCP**: Falhas de conexão são capturadas e reportadas
- **Ferramentas não encontradas**: Mensagens de erro claras quando ferramentas não existem

## Exemplo de Uso com AgentManager

```python
from monkai_agent import AgentManager
from calculator_agent_creator import CalculatorAgentCreator

async def example_with_manager():
    # Criar o agent
    creator = CalculatorAgentCreator()
    agent = await creator.initialize_agent()
    
    # Usar com AgentManager
    manager = AgentManager()
    
    # Executar conversa
    response = await manager.run(
        agent=agent,
        messages=[{"role": "user", "content": "Calcule 25 + 17 e depois multiplique por 3"}],
        debug=True
    )
    
    print(response.messages[-1]["content"])
    
    # Limpeza
    await agent.disconnect_all_clients()
```

## Requisitos

- Python 3.8+
- MonkAI Agent Framework
- Pacote MCP (Model Context Protocol)
- OpenAI ou outro provedor LLM configurado

## Notas Importantes

1. **Ambiente Virtual**: Certifique-se de ativar o ambiente virtual antes de executar
2. **Servidor MCP**: O servidor Calculator é iniciado automaticamente pelo agent
3. **Conexões**: Sempre desconecte os clientes MCP quando terminar para limpeza adequada
4. **Debugging**: Use `debug=True` no AgentManager para ver logs detalhados das operações MCP
