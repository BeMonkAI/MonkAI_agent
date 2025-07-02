# MonkAI Agent Demo com Tracer

Este demo é uma extensão do demo básico do MonkAI Agent, mas com a adição de **observabilidade e tracing** usando Arize Phoenix. Permite monitorar e rastrear todas as interações dos agentes em tempo real através de uma interface web intuitiva.

## 🔍 O que é este Demo?

Este demo contém **exatamente os mesmos agentes** do demo básico:
- **Jornalista Agent** - Especializado em resumir notícias
- **Python Developer Agent** - Focado em desenvolvimento Python  
- **Calculator Agent** - Agente seguro para cálculos matemáticos

**A diferença principal**: Adiciona capacidades completas de observabilidade e tracing para monitorar o comportamento dos agentes.

## 🆚 Diferenças do Demo Básico

### Demo Básico vs Demo Tracer

| Aspecto | Demo Básico | Demo Tracer |
|---------|-------------|-------------|
| **Agentes** | ✅ Mesmos 3 agentes | ✅ Mesmos 3 agentes |
| **Funcionalidade** | ✅ Interação multi-agente | ✅ Interação multi-agente |
| **Observabilidade** | ❌ Apenas logs no terminal | ✅ Interface web completa |
| **Tracing** | ❌ Não disponível | ✅ Rastreamento completo |
| **Análise** | ❌ Limitada | ✅ Métricas e visualizações |
| **Debugging** | ❌ Básico | ✅ Avançado com Phoenix |

## 🔧 Pré-requisitos

### Instalação dos Pacotes Necessários

É **obrigatório** instalar os seguintes pacotes:

```bash
# Pacotes básicos do MonkAI Agent
pip install monkai-agent
pip install monkai-agent-groq

# Pacote para observabilidade e tracing
pip install arize-phoenix

# Instrumentação específica para MonkAI Agent
pip install openinference-instrumentation-monkai-agent
```

### Configuração da API Key

Configure sua chave de API do OpenAI no arquivo `config.py`:

```python
OPENAI_API_KEY_ARTHUR = "sua-chave-openai-aqui"
```

## 🚀 Como Executar

### Passo 1: Ativar Ambiente Virtual
```bash
source .venv/bin/activate
```

### Passo 2: Instalar Dependências
```bash
pip install arize-phoenix
pip install openinference-instrumentation-monkai-agent
```

### Passo 3: Iniciar o Servidor Phoenix (Terminal 1)
```bash
.venv/bin/python -m phoenix.server.main serve
```

Isso iniciará o servidor Phoenix na porta padrão (6006). Você verá uma mensagem como:
```
🚀 Phoenix UI available at http://localhost:6006
```

### Passo 4: Executar o Demo (Terminal 2)
Em um **novo terminal**, execute:
```bash
# Ativar ambiente
source .venv/bin/activate

# Executar demo
cd examples/demo_tracer
python demo.py
```

### Passo 5: Acessar Interface Phoenix
Abra seu navegador e acesse: **http://localhost:6006**

## 📊 Funcionalidades do Tracing

### O que você pode monitorar:

1. **Fluxo de Conversação**
   - Transferências entre agentes
   - Tempo de resposta de cada agente
   - Sequência de chamadas de função

2. **Métricas de Performance**
   - Latência das chamadas de API
   - Tokens utilizados
   - Custos por interação

3. **Debugging Avançado**
   - Logs estruturados
   - Stack traces de erros
   - Análise de prompts e respostas

4. **Visualizações Interativas**
   - Timeline das interações
   - Grafos de dependência
   - Dashboards de métricas

## 🎯 Interface Phoenix

### Principais Seções:

1. **Traces**: Visualiza cada interação completa
2. **Sessions**: Agrupa conversas relacionadas  
3. **Evaluations**: Análise de qualidade das respostas
4. **Datasets**: Dados históricos para análise

### Exemplo de Uso:

1. Execute uma pergunta no demo: *"Calcule 15% de 250"*
2. No Phoenix, você verá:
   - Como o triage direcionou para Calculator Agent
   - Tempo gasto em cada etapa
   - Tokens consumidos
   - Resposta completa estruturada

## 🔧 Configuração do Tracing

### Endpoint de Tracing
```python
endpoint = "http://127.0.0.1:6006/v1/traces"
```

### Instrumentação Habilitada
```python
# Instrumenta todas as chamadas do MonkAI Agent
MonkaiAgentInstrumentor().instrument(tracer_provider=tracer_provider)
```

### Processadores de Span
- **OTLP Exporter**: Envia dados para Phoenix
- **Console Exporter**: Logs no terminal (debug)

## 🛠️ Troubleshooting

### Phoenix não está iniciando
```bash
# Verifique se está instalado
pip list | grep phoenix

# Reinstale se necessário
pip install --upgrade arize-phoenix
```

### Não consegue acessar http://localhost:6006
1. Verifique se o servidor Phoenix está rodando
2. Confirme se não há conflito de porta
3. Tente acessar: http://127.0.0.1:6006

### Traces não aparecem no Phoenix
1. Verifique se o endpoint está correto
2. Confirme que `MonkaiAgentInstrumentor` está instrumentado
3. Execute o demo e faça algumas perguntas

### Erro de Instrumentação
```bash
# Instale novamente a instrumentação
pip install --upgrade openinference-instrumentation-monkai-agent
```

## 📈 Benefícios do Tracing

### Para Desenvolvimento:
- **Debug visual** do fluxo de agentes
- **Identificação de gargalos** de performance
- **Análise de qualidade** das respostas

### Para Produção:
- **Monitoramento em tempo real**
- **Alertas automáticos** para falhas
- **Análise de custos** detalhada
- **Otimização baseada em dados**

## 🎓 Casos de Uso Avançados

### Análise de Performance
```python
# O Phoenix automaticamente coleta:
# - Tempo de resposta por agente
# - Uso de tokens
# - Frequência de transferências
# - Taxa de sucesso
```

### Debugging de Agentes
```python
# Visualize:
# - Por que um agente transferiu para outro
# - Qual prompt foi usado internamente
# - Como as funções foram chamadas
# - Onde ocorreram erros
```

## 📚 Recursos Adicionais

- **Phoenix Documentation**: [docs.arize.com](https://docs.arize.com)
- **OpenInference**: [github.com/Arize-ai/openinference](https://github.com/Arize-ai/openinference)
- **Demo Básico**: `../demo/` (versão sem tracing)

## 🔄 Comparação com Demo Básico

Se você quiser testar **sem tracing**, use o demo básico:
```bash
cd ../demo
python demo.py
```

O demo tracer oferece a **mesma funcionalidade** + observabilidade completa!

---

**💡 Dica**: Use este demo para entender como seus agentes se comportam em produção e otimizar sua performance!
