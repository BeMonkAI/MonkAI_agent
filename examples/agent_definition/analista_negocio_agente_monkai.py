from monkai_agent import Agent, AgentManager 
from monkai_agent.providers import AzureProvider
import asyncio
import config

provider=AzureProvider(
    api_key=config.OPENAI_API_KEY_BRASILSOUTH,
    endpoint=config.OPENAI_AZURE_ENDPOINT_BRASILSOUTH,
    api_version=config.OPENAI_API_VERSION)



manager = AgentManager(provider=provider,model=config.GPT_4o)

agente = Agent(
    name="Agente Analista de Negócios",
    instructions="""
        Você é um Analista de Negócios experiente.
        Sua função é interpretar tendências de mercado, resumir relatórios financeiros 
        e fornecer insights estratégicos de negócios de forma clara e objetiva.

        Você deve:
        - Resumir os principais pontos de documentos financeiros ou relatórios de mercado.
        - Destacar indicadores financeiros relevantes (KPIs).
        - Sugerir decisões estratégicas com base nos dados analisados.
        - Identificar riscos, oportunidades e tendências emergentes.

        Utilize bullet points sempre que possível e evite jargões técnicos.
        Seja direto, claro e foque em recomendações práticas.
    """,
)

result = asyncio.run(manager.run(
    "Resuma os principais insights financeiros dos relatórios econômicos desta semana.",
    agent=agente
))

print(result)
