# Creator e Manager Pattern no MonkAI Agent

Este diretório contém exemplos de implementação do padrão Creator e Manager no framework MonkAI Agent, demonstrando uma abordagem estruturada para criar e gerenciar agentes especializados com camadas de segurança.

## 📚 Conteúdo

O exemplo principal está no notebook `agent_definition_class.ipynb`, que demonstra:
- Criação de agentes especializados
- Gerenciamento de múltiplos agentes
- Implementação de camadas de segurança
- Validação de usuários
- Integração com Azure OpenAI

## 🏗️ Arquitetura

### PythonDeveloperAgentCreator

Uma implementação de agente especializado em desenvolvimento Python que demonstra:

1. **Funcionalidades Principais**:
   - Geração de código Python
   - Criação de arquivos
   - Manipulação de diretórios
   - Validação de usuários

2. **Métodos Implementados**:
   ```python
   def verify_address(self, address)
   def create_python_file(self, path, file_name)
   def write_code_in_file(self, path, file_name, code)
   def replace_code_in_file(self, path, file_name, code)
   ```

### Camada de Segurança

O exemplo implementa um sistema robusto de segurança:

1. **Validação de Usuário**:
   ```python
   def is_user_valid(self):
       if self.user == "valid_user":
           return True
       return False
   ```

2. **Decorador de Validação**:
   ```python
   @validate(is_user_valid)
   def metodo_protegido(self):
       # Método protegido
   ```

## 🚀 Como Executar

### Pré-requisitos

1. **Instalação do MonkAI Agent**:
   ```bash
   pip install monkai_agent
   ```

2. **Configuração do Azure OpenAI**:
   - API Key
   - Endpoint
   - Versão da API
   - Modelo GPT

### Execução do Exemplo

1. **Com Usuário Válido**:
   ```python
   agents_creators = []
   agents_creators.append(PythonDeveloperAgentCreator(user='valid_user'))
   agent_manager = AgentManager(client=client, agents_creators=agents_creators)
   await run_demo_loop(agent_manager)
   ```

2. **Com Usuário Inválido** (para testar segurança):
   ```python
   agents_creators.append(PythonDeveloperAgentCreator(user='usuario_invalido'))
   ```

## 🔒 Sistema de Segurança

### Níveis de Proteção

1. **Validação de Usuário**:
   - Verificação de credenciais
   - Controle de acesso granular

2. **Proteção de Métodos**:
   - Decorador `@validate`
   - Verificação antes da execução

3. **Manipulação Segura de Arquivos**:
   - Validação de caminhos
   - Controle de permissões

## 📋 Estrutura do Código

```
examples/creators_and_manager/
├── agent_definition_class.ipynb    # Implementação principal
└── README.md                       # Esta documentação
```

## 🔍 Funcionalidades do Agente

O PythonDeveloperAgent pode:

1. **Interpretar Requisitos**:
   - Análise de texto do usuário
   - Extração de requisitos de código

2. **Gerar Código**:
   - Criação de classes Python
   - Seguimento de boas práticas
   - Documentação automática

3. **Gerenciar Arquivos**:
   - Criação de arquivos .py
   - Escrita de código
   - Validação de diretórios

## 🛠️ Personalização

Você pode estender este exemplo:

1. **Novos Tipos de Agentes**:
   ```python
   class MeuAgentCreator(MonkaiAgentCreator):
       def __init__(self, user):
           super().__init__()
           # Sua implementação
   ```

2. **Regras de Segurança**:
   - Modifique `is_user_valid`
   - Adicione novas validações
   - Implemente autenticação externa

3. **Funcionalidades Adicionais**:
   - Novos métodos de processamento
   - Integração com outros serviços
   - Logs e monitoramento

## 📝 Boas Práticas

1. **Segurança**:
   - Sempre valide usuários
   - Proteja operações de arquivo
   - Use o decorador `@validate`

2. **Código**:
   - Documente seus métodos
   - Siga padrões PEP 8
   - Implemente tratamento de erros

3. **Gerenciamento**:
   - Use o AgentManager para coordenação
   - Mantenha agentes focados
   - Implemente logging adequado

## 🤝 Contribuição

Para contribuir com melhorias:

1. Faça um fork do repositório
2. Crie sua branch de feature
3. Implemente suas mudanças
4. Envie um pull request

## 📚 Recursos Adicionais

- [Documentação do MonkAI Agent](link_para_documentacao)
- [Guia de Segurança](link_para_guia)
- [Exemplos Adicionais](link_para_exemplos)

---

*Para mais informações, consulte a documentação principal do MonkAI Agent.*
