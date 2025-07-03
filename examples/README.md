# 📚 MonkAI Agent Examples

Esta pasta contém uma coleção abrangente de exemplos práticos demonstrando as diferentes funcionalidades e padrões de uso do framework MonkAI Agent. Cada subdiretório apresenta um aspecto específico do framework, desde conceitos básicos até implementações avançadas.

## 📋 Estrutura dos Examples

### 🎯 [agent_definition/](./agent_definition/)
**Objetivo**: Demonstrar os conceitos fundamentais de criação e definição de agentes.

- **Conteúdo Principal**: 
  - `agent_definition.ipynb` - Notebook interativo com Calculator Agent
  - `analista_negocio_agente_monkai.py` - Implementação de agente analista
- **O que você aprenderá**:
  - Como definir um agente básico
  - Implementar funções personalizadas para agentes
  - Configurar instruções e comportamentos
  - Trabalhar com funções matemáticas (Fibonacci, Bernoulli)

### 🏗️ [creators_and_manager/](./creators_and_manager/)
**Objetivo**: Demonstrar o padrão Creator e Manager para arquiteturas mais complexas.

- **Conteúdo Principal**: 
  - `agent_definition_class.ipynb` - Notebook sobre Creator Pattern
- **O que você aprenderá**:
  - Implementar o padrão Creator para agentes especializados
  - Gerenciar múltiplos agentes simultaneamente
  - Implementar camadas de segurança e validação
  - Integração com Azure OpenAI

### 🚀 [demo/](./demo/)
**Objetivo**: Exemplo prático de múltiplos agentes trabalhando em conjunto.

- **Conteúdo Principal**: 
  - `demo.py` - Demo com 3 agentes especializados
- **Agentes Incluídos**:
  - **Jornalista Agent** - Resumo de notícias
  - **Python Developer Agent** - Desenvolvimento Python
  - **Calculator Agent** - Cálculos matemáticos seguros
- **O que você aprenderá**:
  - Coordenação entre múltiplos agentes
  - Especialização de agentes por domínio
  - Integração com provedor Groq

### 🔍 [demo_tracer/](./demo_tracer/)
**Objetivo**: Demonstrar observabilidade e tracing avançado com Arize Phoenix.

- **Conteúdo Principal**: 
  - `demo.py` - Mesmo demo básico + observabilidade
- **Funcionalidades Adicionais**:
  - Interface web para monitoramento em tempo real
  - Rastreamento completo de interações
  - Métricas e visualizações avançadas
  - Debugging aprimorado
- **O que você aprenderá**:
  - Implementar observabilidade em agentes
  - Monitorar performance e comportamento
  - Usar Arize Phoenix para análise

### 🔌 [mcp_example/](./mcp_example/)
**Objetivo**: Demonstrar integração com Model Context Protocol (MCP) servers.

Esta seção contém múltiplos sub-exemplos:

#### 🧮 [mcp_calculator/](./mcp_example/mcp_calculator/)
- **Funcionalidade**: Agente com capacidades matemáticas via MCP
- **Ferramentas**: Operações básicas, histórico de cálculos
- **Arquivos**: Server MCP, Creator, Demo

#### 🔍 [mcp-duckduckgo/](./mcp_example/mcp-duckduckgo/)
- **Funcionalidade**: Busca web em tempo real via DuckDuckGo
- **Recursos**: Privacidade respeitada, múltiplos formatos de resultado
- **Uso**: Informações atualizadas da web

#### 💾 [mcp-memory/](./mcp_example/mcp-memory/)
- **Funcionalidade**: Sistema de memória persistente
- **Recursos**: Armazenamento e recuperação de contexto

#### 📝 [mcp-notion/](./mcp_example/mcp-notion/)
- **Funcionalidade**: Integração com Notion para gerenciamento de dados
- **Recursos**: Acesso a páginas e bancos de dados do Notion

**O que você aprenderá com MCP**:
- Conectar agentes a serviços externos
- Usar protocolos padronizados para extensibilidade
- Implementar capacidades especializadas via MCP servers

### 🎯 [triage/](./triage/)
**Objetivo**: Demonstrar sistema de triagem inteligente com múltiplos agentes especializados.

- **Conteúdo Principal**: 
  - `triage_example.ipynb` - Notebook de exemplo de triagem
  - Creators especializados para diferentes domínios
- **Agentes Especializados**:
  - `python_developer_agent_creator.py` - Desenvolvimento Python
  - `jornalist_agent_creator.py` - Pesquisa e jornalismo
  - `calculator_agents_creator.py` - Cálculos seguros
- **O que você aprenderá**:
  - Implementar sistema de triagem automática
  - Direcionar consultas para agentes especializados
  - Gerenciar workflow de múltiplos agentes
  - Padrão Manager para coordenação

## 🎯 Progressão Recomendada de Aprendizado

Para obter o máximo proveito dos examples, recomendamos seguir esta sequência:

### 1. **Fundamentos** 📖
Comece com `agent_definition/` para entender os conceitos básicos.

### 2. **Demo Básico** 🚀
Execute `demo/` para ver agentes trabalhando em conjunto.

### 3. **Arquitetura Avançada** 🏗️
Explore `creators_and_manager/` para padrões organizacionais.

### 4. **Observabilidade** 🔍
Implemente tracing com `demo_tracer/` para monitoramento.

### 5. **Integrações Externas** 🔌
Experimente `mcp_example/` para expandir capacidades.

### 6. **Sistema Complexo** 🎯
Finalize com `triage/` para arquiteturas de produção.

## 🛠️ Pré-requisitos Gerais

Antes de executar qualquer exemplo, certifique-se de ter:

### Instalação Base
```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Instalar pacote principal
pip install monkai-agent

# Para exemplos com Groq
pip install monkai-agent-groq
```

### Chaves de API Necessárias
- **OpenAI API Key** (para exemplos básicos)
- **Azure OpenAI** (para examples com Azure)
- **Groq API Key** (para demos com Groq)

### Dependências Opcionais
```bash
# Para observabilidade (demo_tracer)
pip install arize-phoenix

# Para integrações específicas do MCP
pip install mcp  # ou dependências específicas de cada MCP server
```

## 📝 Como Usar

1. **Escolha o exemplo** apropriado para seu nível e objetivo
2. **Leia o README** específico do exemplo escolhido
3. **Configure as chaves de API** necessárias
4. **Execute os pré-requisitos** específicos
5. **Execute o código** seguindo as instruções

## 🤝 Contribuindo

Quer adicionar um novo exemplo? Siga esta estrutura:
- Crie uma nova pasta com nome descritivo
- Inclua um README.md explicativo
- Adicione código bem comentado
- Forneça instruções claras de execução
- Atualize este README principal

## 📚 Recursos Adicionais

- **Documentação Completa**: Veja `DOCUMENTATION.md` na raiz do projeto
- **API Reference**: Explore a pasta `libs/` para detalhes de implementação
- **UI Examples**: Confira `ui/` para interfaces gráficas

---

**💡 Dica**: Cada exemplo é independente, mas conceitos aprendidos em um podem ser aplicados em outros. Experimente, modifique e adapte os exemplos para suas necessidades específicas!
