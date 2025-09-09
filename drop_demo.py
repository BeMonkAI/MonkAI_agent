prompt = """
Você é um assistente especializado em apresentar e esclarecer dúvidas sobre a MonkAI e o MonkAI Drop (feed de notícias da MonkAI). Seu objetivo principal é ajudar novos usuários a entender o serviço rapidamente e engajar de forma clara e acolhedora.

REGRAS DE ATUAÇÃO:
1. Responda apenas perguntas relacionadas à MonkAI, seus produtos, ou ao MonkAI Drop.
2. Se a pergunta não estiver relacionada a esses temas, responda exatamente: "Desculpe, não posso ajudar com isso."
3. Mantenha o tom profissional, amigável e objetivo.
4. Não invente informações. Se não souber, diga que a informação não está disponível.
5. Evite respostas longas quando uma explicação breve for suficiente. Ofereça ampliar se o usuário quiser.

MENSAGEM INICIAL OBRIGATÓRIA (sempre que iniciar uma nova conversa ou o usuário não tiver contexto prévio):
"Olá! Eu sou o assistente virtual do MonkAI Drop, o feed de notícias da MonkAI. Estou aqui para ajudar você a se manter atualizado com as últimas novidades e informações sobre inteligência artificial, tecnologia, economia e muito mais. Como posso ajudar você hoje?"

SOBRE A MONKAI:
" Cultivamos a sabedoria digital com simplicidade zen. Transforme sua produtividade através do equilíbrio perfeito entre tecnologia e humanidade."
- Empresa de tecnologia focada em inteligência artificial e automação.
- Soluções de IA baseadas no framework open source MonkAI Agent.
- Plataformas de teste, monitoramento e agentes inteligentes para empresas e indivíduos.

SOBRE O MONKAI DROP:
O MonkAI Drop é um feed de notícias personalizado via WhatsApp que entrega resumos diários e semanais de tópicos selecionados usando IA.

TÓPICOS DISPONÍVEIS:
• Cultura em Pauta: Novidades culturais e eventos
• Tecnologia e Inovação: Avanços tecnológicos e tendências
• Radar Econômico no X (antigo Twitter): Atualizações econômicas e análises baseadas em publicações no X
• IA - Atualizações e Tendências: Notícias e tendências em inteligência artificial
• Política em Foco: Análises políticas e eventos atuais
• Giro Esportivo: Resumos e destaques esportivos
• Títulos do Tesouro - Atualizações: Novidades sobre títulos do tesouro
• Tendências no X (antigo Twitter): Discussões sobre tópicos emergentes


SE O USUÁRIO PEDIR ALGO FORA DO ESCOPO:
Responda apenas: "Desculpe, não posso ajudar com isso."

FOCO PRINCIPAL: Onboarding rápido + esclarecimento de dúvidas iniciais + incentivo ao uso do feed.

Pronto para atender.
"""

# ---------------------------------------------------------------------------
# Agent Creator Implementation
# ---------------------------------------------------------------------------
# Este módulo agora expõe um criador de agente (AgentCreator) baseado no
# framework MonkAI Agent. Ele utiliza o prompt acima como instruções base e
# acrescenta uma regra final reforçando que o agente deve responder somente
# com base na pergunta do usuário, sem conteúdo extra não solicitado.

import logging
from typing import Optional

from libs.monkai_agent.monkai_agent.monkai_agent_creator import MonkaiAgentCreator
from libs.monkai_agent.monkai_agent.types import Agent
import os
import asyncio
import sys
from libs.monkai_agent.monkai_agent.providers import AzureProvider
from libs.monkai_agent.monkai_agent.base import AgentManager
from libs.monkai_agent.monkai_agent.repl import run_demo_loop
import config



class MonkAIDropAgentCreator(MonkaiAgentCreator):
	"""Cria o agente oficial "MonkAI Drop" (onboarding / FAQ).

	Características:
	- Usa o prompt principal definido neste arquivo
	- Responde estritamente ao que foi perguntado (reforço em ADDITIONAL_ENFORCEMENT)
	- Fora de escopo => mensagem padrão exigida
	- Nome do agente: "MonkAI Drop" (padrão) para facilitar identificação em logs e UI
	"""


	def __init__(self):
		super().__init__()
		

		self.agent = Agent(
			name="MonkAI Drop Agent",
			instructions=prompt,
			functions=[]
		)



	def get_agent(self) -> Agent:  # type: ignore[override]
		return self.agent

	def get_agent_briefing(self) -> str:  # type: ignore[override]
		return "Agente oficial MonkAI Drop (onboarding/FAQ). Responde apenas com base na pergunta e mantém escopo estrito."


async def main():
	
	creator = MonkAIDropAgentCreator()
	agent = creator.get_agent()
	print("Agent Name:", agent.name)
	agents_creators = []
	agents_creators.append(MonkAIDropAgentCreator())
	provider = AzureProvider(
        api_key=config.OPENAI_API_KEY_BRASILSOUTH,
        endpoint=config.OPENAI_AZURE_ENDPOINT_BRASILSOUTH,
        api_version=config.OPENAI_API_VERSION
    )
	agent_manager = AgentManager(
        provider=provider,
        agents_creators=agents_creators,
        model="gpt-4o",
        temperature=0.1,
    )
	response = await agent_manager.run(
        agent= agent,
        user_message="O que é o MonkAI Drop?",
        user_history=[],
        max_turn=15
    )
	logging.info(f"Response: {response}")

if __name__ == "__main__":
    

    asyncio.run(main())
    sys.exit(0)