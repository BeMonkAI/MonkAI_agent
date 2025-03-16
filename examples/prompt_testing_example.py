"""
Example demonstrating how to use the prompt testing and optimization features of MonkAI.
This example compares different prompts for a complex query.
"""

import asyncio
import os
from openai import OpenAI, AzureOpenAI
from monkai_agent import Agent, PromptTest, PromptOptimizerManager, AgentManager
from typing import List, Dict
import json
import config

async def generate_enhanced_prompt(client: OpenAI, base_prompts: Dict[str, str], model: str = 'gpt-4o') -> str:
    """Generate an enhanced prompt using AI by analyzing existing prompts."""
    prompt_analysis = "\n".join([
        f"Prompt {i+1}:\n{prompt}\n"
        for i, prompt in enumerate(base_prompts.values())
    ])
    
    messages = [
        {"role": "system", "content": "You are an expert in prompt engineering and optimization."},
        {"role": "user", "content": f"""Analyze these prompts and create an enhanced version that combines their strengths:
        
{prompt_analysis}

Create a new prompt that:
1. Synthesizes the best aspects of all prompts
2. Adds improvements and optimizations
3. Maintains clarity and structure
4. Is more comprehensive and effective

Format the response as a complete system prompt."""}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

async def main():
    # Get API key from environment variable
    #api_key = os.getenv('OPENAI_API_KEY')
    #if not api_key:
    #    print("Error: OPENAI_API_KEY environment variable is not set")
    #    return
    
    # Initialize OpenAI client
    client = AzureOpenAI(
            api_key=config.OPENAI_API_KEY_BRASILSOUTH,
            api_version=config.GPT4o_OPENAI_API_VERSION_BRASILSOUTH,
            azure_endpoint=config.OPENAI_AZURE_ENDPOINT_BRASILSOUTH,
        )
    
    # Define different prompts to test
    base_prompts = {
        "gemini": """*Função:* Agente especializado na verificação de informações para preenchimento de contratos.

*Campos a serem verificados (Informações Necessárias):*

*Obrigatórios ():**
•⁠  ⁠CNPJ/CPF (*)
•⁠  ⁠Planta (*)
•⁠  ⁠Condição de Pagamento (*)
•⁠  ⁠Forma de Pagamento (*)
•⁠  ⁠Código do Material (*)
•⁠  ⁠Cadência (*)

*Opcionais:*
•⁠  ⁠Vendedor
•⁠  ⁠E-mail do Vendedor
•⁠  ⁠Cidade
•⁠  ⁠Data de Negociação
•⁠  ⁠Incoterms
•⁠  ⁠Preço

*Regras de Operação:*

1.⁠ ⁠*Informações Obrigatórias:*
    - Se um campo obrigatório () estiver faltando, **solicite ao usuário que forneça a informação faltante.* Interrompa o processo até receber o dado.
    - Caso contrário, continue para a verificação dos dados fornecidos.

2.⁠ ⁠*Verificação e Correção de Informações:*
    - Para cada campo fornecido pelo usuário, realize a verificação utilizando a função correspondente.
    - *Se um campo estiver incorreto ou incompleto:*
        - Solicite a correção ao usuário.
        - Após a correção, utilize a função correspondente para verificar e atualizar o campo.
        - *Peça confirmação ao usuário APENAS se a correção for realizada por um subagente.* Solicite a confirmação um campo por vez.
        - Se o campo estiver correto, continue o processo.
    - *Exceção:* O campo 'Cadência' não necessita de confirmação do usuário. Atualize o campo diretamente e continue o processo.

    *Verificações Específicas:*
    - *Cliente (Vendedor/CNPJ/CPF):* Se necessário atualizar informações do cliente, utilize o arquivo CSV. Solicite as informações ao usuário uma de cada vez.
    - *Forma de Pagamento:* Utilize a função ⁠ check_payment_method ⁠ para verificar e corrigir.
    - *Condição de Pagamento:* Utilize a função ⁠ check_payment_terms ⁠ para verificar e corrigir.
    - *Código do Material:* Utilize a função ⁠ check_material ⁠ para verificar e corrigir.
    - *Cadência:* Utilize a função ⁠ check_cadencia ⁠ para verificar e corrigir o formato.

3.⁠ ⁠*Confirmação Final:*
    - Após verificar todos os campos fornecidos e garantir que as informações obrigatórias estão completas e corretas, apresente um *resumo final do formulário* ao usuário para confirmação.

4.⁠ ⁠*Geração de Incidente:*
    - Após a confirmação final do usuário, utilize a função ⁠ create_incident ⁠ para gerar um código de rastreamento (incidente) da solicitação e envie-o ao usuário. *Conclua o processo.*

*Limites de Atuação:*

•⁠  ⁠*Escopo Restrito:* Concentre-se EXCLUSIVAMENTE na verificação e validação das informações fornecidas pelo usuário para o contrato.
•⁠  ⁠*Não responda a perguntas fora do escopo.* Se o usuário fizer perguntas ou comentários não relacionados à verificação de dados para o contrato, utilize a função ⁠ transfer_to_triage ⁠.
•⁠  ⁠*Confidencialidade do Processo Interno:* Mantenha o processo de verificação e correção interno. *Não comunique os detalhes do processo ao usuário.* Apresente apenas as respostas ou solicitações de informação necessárias.
•⁠  ⁠*Redirecionamento para Triagem:* Se o usuário solicitar informações fora do escopo, utilize ⁠ transfer_to_triage ⁠. Se não houver agente adequado, informe que você não pode ajudar e aguarde novas instruções do agente de triagem.

""","copilot":"""Você é um agente especializado em verificação e validação de contratos. Sua missão é garantir a precisão e completude das informações contratuais, seguindo um processo estruturado de validação.

                CAMPOS DO CONTRATO:
                Campos Obrigatórios (*):
                - CNPJ/CPF (*)
                - Planta (*)
                - Condição de Pagamento (*)
                - Forma de Pagamento (*)
                - Código do Material (*)
                - Cadência (*)

                Campos Opcionais:
                - Vendedor
                - E-mail do Vendedor
                - Cidade
                - Data de Negociação
                - Incoterms
                - Preço

                PROCESSO DE VALIDAÇÃO:

                1. Verificação Inicial
                   - Identifique campos obrigatórios faltantes
                   - Solicite imediatamente os campos ausentes
                   - Prossiga apenas com todos os campos obrigatórios preenchidos

                2. Validação Sequencial
                   - Verifique cada campo na ordem estabelecida
                   - Use funções específicas para validação:
                     > Cliente/CNPJ: verify_client()
                     > Planta: check_plant()
                     > Forma de Pagamento: check_payment_method()
                     > Condição de Pagamento: check_payment_terms()
                     > Código do Material: check_material()
                     > Cadência: check_cadencia()

                3. Processo de Correção
                   - Ao identificar erro, corrija um campo por vez
                   - Solicite confirmação do usuário para cada correção
                   - Exceção: campo 'Cadência' não requer confirmação
                   - Mantenha registro das correções no metadata

                4. Atualizações no Sistema
                   - Dados do cliente: Atualize o CSV quando necessário
                   - Solicite informações complementares uma por vez
                   - Mantenha o usuário informado sobre atualizações

                5. Finalização
                   - Apresente resumo final dos dados validados
                   - Solicite confirmação do usuário
                   - Gere código de rastreamento via create_incident()
                   - Informe o código ao usuário

                REGRAS DE INTERAÇÃO:

                1. Comunicação
                   - Seja conciso e direto
                   - Evite explicar processos internos
                   - Foque nas informações relevantes ao usuário
                   - Use linguagem profissional e clara

                2. Gestão de Erros
                   - Identifique erros específicos
                   - Forneça orientações claras para correção
                   - Mantenha o contexto da conversa
                   - Evite repetições desnecessárias

                3. Limites de Atuação
                   - Mantenha-se no escopo de validação contratual
                   - Redirecione questões não relacionadas para transfer_to_triage
                   - Não forneça informações sobre outros processos
                   - Mantenha confidencialidade das operações internas

                4. Validações Específicas
                   - CNPJ/CPF: Formato e existência no sistema
                   - Planta: Valores permitidos (SRS, PDL, LRV, 163)
                   - Pagamentos: Códigos e condições válidas
                   - Material: Códigos existentes
                   - Cadência: Formato MM.AAAA:quantidade

                OBSERVAÇÕES IMPORTANTES:
                - Mantenha o fluxo de verificação contínuo
                - Não revele processos internos ao usuário
                - Priorize a validação de campos obrigatórios
                - Garanta a integridade dos dados antes de finalizar
            """
    }
    
    # Enable/disable AI prompt generation
    AI_PROMPT_GENERATE = True
    
    # Generate enhanced prompt if enabled
    prompts = base_prompts.copy()
    if AI_PROMPT_GENERATE:
        print("\nGenerating AI-enhanced prompt...")
        enhanced_prompt = await generate_enhanced_prompt(client, base_prompts, config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH)
        prompts["AI-Enhanced Expert"] = enhanced_prompt
        print("AI-enhanced prompt generated successfully!")
    
    # Create a complex test case
    test_cases = [
        PromptTest(
            name="Test Case 1",
            input_text="Ola, Vendedor: REGINALDO CAMPOS, CNPJ/CPF:33300904874, Cidade:PATROCINIO, Planta:163, Condição de pagamento: F090, Forma de pagamento: A, Código do material: 300004, Cadência: 03.2025:150,04.2025:255",
            expected_output="Nao existe o cliente com o CNPJ/CPF 33300904874",
            memory=None
        ),
        PromptTest(
            name="Test Case 2",
            input_text="Quero fazer um test da poc de fs",
            expected_output="Por favor, forneça as seguintes informações para preenchimento do contrato:\n\n- CNPJ/CPF ()\n- Planta ()\n- Condição de Pagamento ()\n- Forma de Pagamento ()\n- Código do Material ()\n- Cadência ()\n\nOs demais campos são opcionais."
        ),
        PromptTest(
            name="Test Case 3",
            input_text="Vendedor: REGINALDO CAMPOS\nCNPJ/CPF:01.614.771/0001-31\nCidade:PATROCINIO\nEmail do vendedor:reginaldo.campos@fs.agr.br\nPlanta:LRV\nNome do cliente:RICARDO TEJADA DE ARAUJO\nCódigo do cliente:027.535.302-89\nData da negociação:25/02/2025\nPreço:1745\nCódigo do material:300004\nCadência:\n03.2025:150,04.2025:200,05.2025:90",
            expected_output="As informações obrigatórias 'Condição de Pagamento' e 'Forma de Pagamento' estão faltando. Por favor, forneça esses dados para continuar."
        ),
        PromptTest(
            name="Test Case 4",
            input_text="Condicao de pagamente : barter semente e forma de pagamento boleto",
            expected_output="Por favor, forneça os seguintes campos obrigatórios:\n- CNPJ/CPF\n- Planta\n- Código do Material\n- Cadência"
        ),
        PromptTest(
            name="Test Case 5",
            input_text="Vendedor: REGINALDO CAMPOS\nCNPJ/CPF:01.614.771/0001-31\nCidade:PATROCINIO\nEmail do vendedor:reginaldo.campos@fs.agr.br\nPlanta:LRV\nNome do cliente:RICARDO TEJADA DE ARAUJO\nCódigo do cliente:027.535.302-89\nData da negociação:25/02/2025\nPreço:1745\nCódigo do material:300004\nCadência:\n03.2025:150,04.2025:200,05.2025:90",
            expected_output="Você não forneceu as informações obrigatórias para os seguintes campos: Condição de Pagamento e Forma de Pagamento. Por favor, forneça esses dados para que possamos continuar."
        ),
        PromptTest(
            name="Test Case 6",
            input_text="Condicao de pagamente : barter semente e forma de pagamento boleto",
            expected_output="Por favor, forneça as seguintes informações obrigatórias que estão faltando:\n\n- CNPJ/CPF\n- Planta\n- Código do Material\n- Cadência"
        ),
        PromptTest(
            name="Test Case 7",
            input_text="Vendedor: REGINALDO CAMPOS\nCNPJ/CPF:01.614.771/0001-31\nCidade:PATROCINIO\nEmail do vendedor:reginaldo.campos@fs.agr.br\nPlanta:LRV\nNome do cliente:RICARDO TEJADA DE ARAUJO\nCódigo do cliente:027.535.302-89\nData da negociação:25/02/2025\nPreço:1745\nCódigo do material:300004\nCadência:\n03.2025:150,04.2025:200,05.2025:90",
            expected_output="A condição de pagamento fornecida 'barter semente' corresponde a 'ZBTS (Barter Sementes)'.\n\nPor favor, confirme se essa condição de pagamento está correta."
        ),
        PromptTest(
            name="Test Case 8",
            input_text="Esta",
            expected_output="A forma de pagamento fornecida 'boleto' corresponde a 'Boleto Bancário'.\n\nPor favor, confirme se essa forma de pagamento está correta."
        ),
        PromptTest(
            name="Test Case 9",
            input_text="Esta",
            expected_output="Aqui está o resumo final do formulário com todas as informações corrigidas:\n\n- Vendedor: REGINALDO CAMPOS\n- CNPJ/CPF: 01.614.771/0001-31\n- E-mail do Vendedor: reginaldo.campos@fs.agr.br\n- Planta: LRV\n- Cidade: PATROCINIO\n- Condição de Pagamento: ZBTS (Barter Sementes)\n- Forma de Pagamento: Boleto Bancário\n- Data de Negociação: 25/02/2025\n- Incoterms: Não fornecido\n- Preço: 1745\n- Código do Material: 300004\n- Cadência: 03.2025:150,04.2025:200,05.2025:90\n\nPor favor, confirme se todas as informações estão corretas."
        ),
        PromptTest(
            name="Test Case 10",
            input_text="Sim",
            expected_output="A solicitação foi concluída com sucesso. O código de rastreio da sua solicitação é: S0325-1123.\n\nGuarde este código para futuras consultas.\n\nSe precisar de mais alguma coisa, estou à disposição!"
        ) 
    ]
    
    # Create agent manager
    agent_manager = AgentManager(client=client, agents_creators=[])
    results = []
    for test_case in test_cases:
        print("\nComplex Query Comparison")
        print("=" * 80)
        print(f"User Message: {test_case.input_text}")
        print("\nResponses from different prompts:")
        print("-" * 80)

        results_data = {}
        for prompt_name, prompt_text in prompts.items():
            try:
                # Create agent with current prompt
                agent = Agent(
                    name=f"TestAgent_{prompt_name}",
                    instructions=prompt_text,
                    model=config.GPT4o_OPENAI_GPT_MODEL_BRASILSOUTH
                )
                agent_manager.agent = agent
                
                # Run test
                messages = [{"role": "user", "content": test_case.input_text}]
                response = agent_manager.get_chat_completion(
                    agent=agent,
                    history=messages,
                    context_variables={},
                    model_override=None,
                    temperature=0.7,
                    max_tokens=150,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0,
                    stream=False,
                    debug=False
                )
                
                # Print results
                print(f"\n{prompt_name}:")
                print(f"System Prompt: {prompt_text}")
                
                #Iterate over test cases
                print(f"User Message: {test_case.input_text}")
                print(f"Answer: {response.choices[0].message.content}")
                print("-" * 80)
                
                # Store results
                results_data[prompt_name] = {
                    "system_prompt": prompt_text,
                    "input": test_case.input_text,
                    "response": response.choices[0].message.content
                }
                
            except Exception as e:
                print(f"\nError with {prompt_name}:")
                print(f"System Prompt: {prompt_text}")
                print(f"Error message: {str(e)}")
                print("-" * 80)
                results_data[prompt_name] = {
                    "system_prompt": prompt_text,
                    "input": test_case.input_text,
                    "error": str(e)
                }
            results.append(results_data)
    
    # Save results to JSON for reference
    with open("complex_query_comparison.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nResults have been saved to 'complex_query_comparison.json'")

if __name__ == "__main__":
    asyncio.run(main())