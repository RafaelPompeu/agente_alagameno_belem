from google.adk.agents import Agent
from google.adk.tools import google_search
from .utils import call_agent

MODEL_NAME = "gemini-2.0-flash"

def agente_tabua_mare(local: str, data_alvo: str) -> str:
    local = "Belém"  # força sempre Belém
    instruction_text = f"""
    Você é um especialista em marés e utiliza a ferramenta Google Search.
    Sua tarefa é fornecer a tábua da maré (horários de maré alta e baixa, com alturas em metros) para o local e data informados.

    Formato da Resposta:
    Maré alta: HH:MM (X.Ym), HH:MM (X.Ym)
    Maré baixa: HH:MM (X.Ym), HH:MM (X.Ym)

    Se alguma informação (horário ou altura) não estiver disponível, indique "sem informação" para o item específico.
    Se não houver dados para maré alta ou baixa como um todo, informe "Maré alta: sem informação" ou "Maré baixa: sem informação".

    Dados para a consulta:
    Local: {local}
    Data: {data_alvo}
    """
    agente = Agent(
        name="agente_tabua_mare",
        model=MODEL_NAME,
        instruction=instruction_text,
        description="Agente para buscar a tábua da maré (horários e alturas) via Google Search.",
        tools=[google_search]
    )
    entrada = f"Qual a tábua da maré para {local} em {data_alvo}, incluindo horários e alturas das marés alta e baixa?"
    return call_agent(agente, entrada)
