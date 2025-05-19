from google.adk.agents import Agent
from .utils import call_agent

MODEL_NAME = "gemini-2.0-flash"

def agente_analise_risco_alagamento(
    bairro: str,
    cidade: str,
    previsao_chuva: str,
    tabua_mare: str,
    lista_pontos_criticos,
    altitude_bairro: str,
    api_key=None
) -> str:
    cidade = "Belém"  # força sempre Belém
    # Monta string de pontos críticos do bairro
    if bairro:
        pontos_bairro = [p for p in lista_pontos_criticos if bairro in p.get("bairro", "")]
        pontos_str = "; ".join(
            f"{p['bairro']} ({p['tipo_alagamento']}, risco {p['risco']})"
            for p in pontos_bairro
        ) if pontos_bairro else "Nenhum ponto crítico registrado para o bairro."
    else:
        pontos_str = "; ".join(
            f"{p['bairro']} ({p['tipo_alagamento']}, risco {p['risco']})"
            for p in lista_pontos_criticos
        ) if lista_pontos_criticos else "Nenhum ponto crítico registrado."
    instruction_text = f"""
    Você é um analista de risco de alagamento.
    Sua função é avaliar o risco de alagamento para o bairro '{bairro}' na cidade de Belém com base nos dados fornecidos.
    Classifique o risco como: BAIXO, MÉDIO, ALTO ou MUITO ALTO.
    Forneça uma justificativa concisa para sua avaliação, considerando a combinação dos fatores.

    Dados para Análise:
    - Bairro: {bairro}
    - Cidade: {cidade}
    - Previsão de Chuva (para a data relevante): {previsao_chuva}
    - Tábua da Maré (para a data relevante): {tabua_mare}
    - Pontos Críticos Conhecidos: {pontos_str}
    - Altitude Média: {altitude_bairro}

    Diretrizes para Avaliação do Risco:
    - **MUITO ALTO RISCO**: Combinação crítica de fatores: chuva forte/muito forte, maré alta significativa (especialmente se coincidente com picos de chuva), presença de muitos pontos críticos ou histórico grave, e/ou altitude muito baixa.
    - **ALTO RISCO**: Presença de múltiplos fatores de risco: chuva moderada a forte, maré alta, pontos críticos conhecidos ou baixa altitude.
    - **MÉDIO RISCO**: Alguns fatores de risco presentes: chuva leve a moderada, maré normal a alta (sem extremos), e/ou vulnerabilidade conhecida.
    - **BAIXO RISCO**: Ausência de fatores de risco significativos: sem previsão de chuva expressiva, maré normal ou baixa, poucos pontos críticos e/ou altitude que não sugere vulnerabilidade.

    Considerações Adicionais:
    - Se a altitude for "sem informação", mencione isso na justificativa e baseie a análise nos outros fatores, indicando que a ausência dessa informação pode impactar a precisão.
    - A coincidência temporal de chuva intensa e maré alta eleva significativamente o risco.

    Formato da Resposta:
    [NÍVEL DE RISCO] de alagamento em {bairro if bairro else cidade}.
    Justificativa: [Explicação concisa baseada nos dados, diretrizes e considerações]
    """
    agente = Agent(
        name="agente_analise_risco_alagamento",
        model=MODEL_NAME,
        instruction=instruction_text,
        description="Agente analítico para determinar o nível de risco de alagamento e justificar.",
        tools=[]
    )
    entrada = f"Com base nos dados fornecidos, qual o nível de risco de alagamento para o bairro '{bairro}' em Belém e por quê?"
    return call_agent(agente, entrada, api_key=api_key)
