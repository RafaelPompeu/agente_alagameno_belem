from google.adk.agents import Agent
from google.adk.tools import google_search
from .utils import call_agent

MODEL_NAME = "gemini-2.0-flash"

def agente_altitude_bairro(bairro: str, cidade: str, api_key=None) -> str:
    cidade = "Belém"  # força sempre Belém
    if bairro:
        local = f"{bairro}, {cidade}"
    else:
        local = cidade
    instruction_text = f"""
    Você é um assistente geográfico que utiliza Google Search.
    Sua tarefa é encontrar a altitude média aproximada de {local}.
    Responda APENAS o valor em metros (ex: "8 metros").
    Se a informação não for encontrada de forma confiável, responda "sem informação".
    """
    agente = Agent(
        name="agente_altitude_bairro",
        model=MODEL_NAME,
        instruction=instruction_text,
        description="Agente para buscar a altitude média de uma cidade ou bairro via Google Search.",
        tools=[google_search]
    )
    entrada = f"Qual é a altitude média de {local}?"
    return call_agent(agente, entrada, api_key=api_key)
