from mcp.server import Server
import mcp.types as types

# Define available prompts
PROMPTS = {
    "saudacao": types.Prompt(
        name="saudacao",
        description="faz uma saudação ao usuáro e explica o que o agente faz",
        arguments=[
            types.PromptArgument(
                name="agente",
                description="qual agente está sendo usado",
                required=False
            ),
            types.PromptArgument(
                name="tipo",
                description="Tipo de saudação: 'formal' ou 'informal'",
                required=True
            )
        ],
    ),
}
