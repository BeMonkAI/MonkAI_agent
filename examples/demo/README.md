# MonkAI Agent Demo

Este demo mostra a interação de múltiplos agentes especializados usando o framework MonkAI Agent. O exemplo demonstra como três diferentes tipos de agentes podem trabalhar em conjunto para atender diversas solicitações do usuário.

## 🤖 Agentes Incluídos

O demo inclui três agentes especializados:

1. **Jornalista Agent** - Especializado em resumir notícias e informações de jornais
2. **Python Developer Agent** - Focado em desenvolvimento Python e soluções técnicas
3. **Calculator Agent** - Agente seguro para realizar cálculos matemáticos

## 🔧 Pré-requisitos

### Instalação dos Pacotes Necessários

É **obrigatório** instalar os seguintes pacotes antes de executar o demo:

```bash
# Instalar o pacote principal MonkAI Agent
pip install monkai-agent

# Instalar o provedor Groq para MonkAI Agent
pip install monkai-agent-groq
```

### Configuração da API Key

Você precisará de uma chave de API do Groq. Substitua `"my-api-key"` no código pela sua chave real:

```python
provider = GroqProvider("sua-chave-api-aqui")
```

### Ambiente Virtual (Recomendado)

O projeto já contém um ambiente virtual local. Ative-o antes de executar:

```bash
source .venv/bin/activate
```

## 🚀 Como Executar

1. **Clone o repositório e navegue até o diretório do demo:**
   ```bash
   cd examples/demo
   ```

2. **Ative o ambiente virtual:**
   ```bash
   source .venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install monkai-agent monkai-agent-groq
   ```

4. **Configure sua API Key do Groq no código**

5. **Execute o demo:**
   ```bash
   python demo.py
   ```

## 🎯 Funcionalidades

### Sistema de Triage Inteligente

O demo utiliza um sistema de triage que automaticamente:
- Identifica qual agente é mais adequado para cada solicitação
- Redireciona conversas para o agente especializado apropriado
- Permite transferência entre agentes quando necessário

### Interação Multi-Agente

Os agentes podem:
- Trabalhar independentemente em suas especialidades
- Transferir conversas entre si quando necessário
- Colaborar para resolver problemas complexos

### Modelo Configurável

O demo usa o modelo `llama-3.3-70b-versatile` do Groq com:
- Temperatura: 0.3 (para respostas mais consistentes)
- Debug habilitado para observar o funcionamento interno

## 📝 Estrutura do Código

```python
# Importação dos agentes especializados
from examples.triage.python_developer_agent_creator import PythonDeveloperAgentCreator
from examples.triage.jornalist_agent_creator import JornalistAgentCreator
from examples.triage.calculator_agents_creator import CalculatorAgentCriator

# Configuração do provedor e modelo
provider = GroqProvider("my-api-key")
agent_manager = AgentManager(
    provider=provider, 
    agents_creators=agents_creators, 
    model="llama-3.3-70b-versatile", 
    temperature=0.3
)
```

## 🔍 Exemplo de Uso

Após executar o demo, você pode interagir com os agentes fazendo perguntas como:

- **Para o Jornalista:** "Resuma as principais notícias de hoje"
- **Para o Desenvolvedor Python:** "Como posso implementar uma API REST em Python?"
- **Para a Calculadora:** "Calcule 15% de 250"

O sistema automaticamente direcionará cada pergunta para o agente mais apropriado.

## 🛠️ Personalização

Para adicionar novos agentes ao demo:

1. Crie uma nova classe que herde de `TransferTriageAgentCreator`
2. Implemente os métodos necessários
3. Adicione o agente à lista `agents_creators` no demo

## 📚 Recursos Adicionais

- **Documentação completa:** Consulte o arquivo `DOCUMENTATION.md` na raiz do projeto
- **Mais exemplos:** Explore o diretório `examples/` para outros casos de uso
- **Testes:** Execute os testes em `tests/` para validar a instalação

## 🐛 Troubleshooting

### Erro de Importação
Se encontrar erros de importação, certifique-se de que:
- Os pacotes `monkai-agent` e `monkai-agent-groq` estão instalados
- O ambiente virtual está ativado
- Você está executando o script do diretório correto

### Erro de API Key
- Verifique se sua chave do Groq está correta
- Confirme se você tem créditos disponíveis na sua conta Groq

### Problemas de Dependências
```bash
# Reinstalar dependências
pip install -r requirements.txt
```

## 📄 Licença

Este projeto está licenciado sob os termos especificados no arquivo LICENSE na raiz do repositório.
