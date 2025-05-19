from google.adk.agents import Agent
from google.adk.tools import google_search
from google.genai import types
from .utils import call_agent

MODEL_NAME = "gemini-2.0-flash"

def agente_previsao_chuva(cidade: str, data_alvo: str, api_key=None) -> str:
    cidade = "Belém"  # força sempre Belém
    instruction_text = f"""
    Você é um assistente meteorológico preciso que utiliza a ferramenta Google Search.
    Sua tarefa é buscar a previsão de chuva para a cidade e data fornecidas.
    Organize a resposta estritamente nos seguintes períodos, indicando a intensidade da chuva (leve, moderada, forte, muito forte) ou "sem chuva":
    - Manhã (06:00-12:00)
    - Tarde (12:00-18:00)
    - Noite (18:00-00:00)
    - Madrugada (00:00-06:00)

    Se não houver dados para um período específico, informe "sem informação".

    Exemplo de Resposta:
    Manhã: sem chuva
    Tarde: chuva forte
    Noite: chuva moderada
    Madrugada: sem informação

    Dados para a consulta:
    Cidade: {cidade}
    Data: {data_alvo}
    """
    agente = Agent(
        name="agente_previsao_chuva",
        model=MODEL_NAME,
        instruction=instruction_text,
        description="Agente para buscar previsão de chuva (horários e intensidade) via Google Search.",
        tools=[google_search]
    )
    entrada = f"Qual a previsão de chuva para {cidade} em {data_alvo}, detalhada por período (manhã, tarde, noite, madrugada) e intensidade?"
    return call_agent(agente, entrada, api_key=api_key)
