from google.adk.agents import Agent
from google.adk.tools import google_search
from .utils import call_agent

MODEL_NAME = "gemini-2.0-flash"

def agente_pontos_criticos_alagamento(cidade: str, caminho_arquivo_txt: str, api_key=None):
    cidade = "Belém"  # força sempre Belém
    pontos = []
    try:
        with open(caminho_arquivo_txt, 'r', encoding='utf-8') as f:
            bloco = {}
            for linha in f:
                l = linha.strip()
                if l.startswith("==== PDF"):
                    if bloco:
                        pontos.append(bloco)
                    bloco = {}
                elif "Bairro:" in l or "Bairros:" in l or "Distrito de" in l:
                    # Extrai bairros
                    if "Bairros:" in l:
                        bairros = l.split("Bairros:")[1].split("–")[0].replace(":", "").strip()
                    elif "Bairro:" in l:
                        bairros = l.split("Bairro:")[1].split("–")[0].replace(":", "").strip()
                    else:
                        bairros = l
                    bloco["bairro"] = bairros
                elif "Tipologia do Processo:" in l:
                    tipos = l.split("Tipologia do Processo:")[1].strip()
                    bloco["tipo_alagamento"] = tipos
                elif "Grau de risco:" in l:
                    risco = l.split("Grau de risco:")[1].strip()
                    bloco["risco"] = risco
            if bloco:
                pontos.append(bloco)
    except FileNotFoundError:
        print(f"AVISO: Arquivo de pontos críticos '{caminho_arquivo_txt}' não encontrado.")

    # Remove duplicados por bairro e tipo
    resultado = []
    vistos = set()
    for p in pontos:
        bairro = p.get("bairro", "").strip()
        tipo = p.get("tipo_alagamento", "").strip()
        risco = p.get("risco", "").strip()
        chave = (bairro, tipo, risco)
        if bairro and tipo and chave not in vistos:
            resultado.append({
                "bairro": bairro,
                "tipo_alagamento": tipo,
                "risco": risco
            })
            vistos.add(chave)
    return resultado

    exemplos_oficiais_texto = (
        "Considere também os seguintes exemplos de pontos críticos de referência e seus riscos associados:\n"
        "- Passagem Tradição - Comunidade Fé em Deus II: risco ALTO de inundação, ~150 famílias afetadas.\n"
        "- Av. Beira Mar - Ilha do Outeiro: risco MUITO ALTO de erosão costeira.\n"
        "- Praia Belo Paraíso: risco MUITO ALTO de erosão costeira e inundações.\n"
        "- Distrito de Icoaraci: risco MUITO ALTO de alagamento.\n"
        "- Áreas como Paracuri, Parque Guajará, Conj. Tocantins, Vila Riso, Buraco Fundo, Canarinho, Piçarreira: risco de inundação recorrente (Fev-Maio)."
    )

    texto_pontos_locais_formatado = ""
    if pontos_locais:
        texto_pontos_locais_formatado = (
            "Adicionalmente, foram registrados os seguintes pontos críticos localmente (a partir do arquivo fornecido):\n"
            + "\n".join(f"- {p}" for p in pontos_locais)
        )

    instruction_text = f"""
    Você é um assistente de pesquisa focado em identificar áreas de risco de alagamento em {cidade}, utilizando Google Search e dados fornecidos.
    Sua tarefa é consolidar uma lista de comunidades ou pontos críticos suscetíveis a alagamentos.
    Priorize informações de fontes oficiais (prefeitura, defesa civil) obtidas pela busca.

    {exemplos_oficiais_texto}
    {texto_pontos_locais_formatado if texto_pontos_locais_formatado else "Nenhum ponto crítico adicional foi fornecido de arquivos locais."}

    Instruções para a Resposta:
    1. Use o Google Search para encontrar a lista mais atualizada de pontos críticos em {cidade} de fontes oficiais.
    2. Complemente com as informações de referência e do arquivo local (se fornecidas acima).
    3. Liste SOMENTE os nomes das comunidades ou locais críticos.
    4. NÃO repita nomes. Consolide as informações.
    5. Se dados sobre o número de pessoas/famílias afetadas ou o nível de risco (ex: alto, muito alto) estiverem explicitamente associados a um local nas fontes ou nos dados fornecidos, inclua essa informação entre parênteses.

    Exemplo de Formato de Resposta:
    - Passagem Tradição - Comunidade Fé em Deus II (risco ALTO, ~150 famílias afetadas)
    - Av. Beira Mar - Ilha do Outeiro (risco MUITO ALTO)
    - Paracuri (risco MUITO ALTO, inundação recorrente Fev-Maio)
    - [Nome do Ponto do Arquivo Local 1]
    """
    agente = Agent(
        name="agente_pontos_criticos_alagamento",
        model=MODEL_NAME,
        instruction=instruction_text,
        description="Agente para identificar pontos críticos de alagamento, combinando busca online com dados fornecidos.",
        tools=[google_search]
    )
    entrada = f"Liste os pontos críticos de alagamento em {cidade}, com base em dados oficiais, estudos e registros fornecidos."
    return call_agent(agente, entrada, api_key=api_key)
