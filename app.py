from flask import Flask, render_template, request, redirect, url_for, flash
import os
# Importa os agentes reais
from agentes.previsao_chuva import agente_previsao_chuva
from agentes.tabua_mare import agente_tabua_mare
from agentes.pontos_criticos import agente_pontos_criticos_alagamento
from agentes.altitude_cidade import agente_altitude_bairro
from agentes.analise_risco import agente_analise_risco_alagamento
from datetime import date
app = Flask(__name__)

def ler_pontos_criticos(caminho_arquivo):
    pontos = []
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, encoding="utf-8") as f:
            for linha in f:
                l = linha.strip()
                if l:
                    pontos.append(l)
    return pontos

BAIRROS_COORDS = {
    "Terra Firme": {"lat": -1.459, "lng": -48.457},
    "Umarizal": {"lat": -1.445, "lng": -48.483},
    "Marco": {"lat": -1.441, "lng": -48.469},
    "Batista Campos": {"lat": -1.4608, "lng": -48.4889},
    "Jurunas": {"lat": -1.467, "lng": -48.498},
    "Guamá": {"lat": -1.465, "lng": -48.475},
    "Cremação": {"lat": -1.458, "lng": -48.480}
}

@app.route("/", methods=["GET", "POST"])
def home():
    cidade_alvo = "Belém"
    data_alvo = date.today().strftime("%Y-%m-%d")
    caminho_arquivo_riscos = os.path.join(os.path.dirname(__file__), "riscos-geologicos.txt")
    previsao_chuva_info = agente_previsao_chuva(cidade_alvo, data_alvo)
    tabua_mare_info = agente_tabua_mare(cidade_alvo, data_alvo)
    pontos_criticos_info = agente_pontos_criticos_alagamento(cidade_alvo, caminho_arquivo_riscos)
    bairros = list(BAIRROS_COORDS.keys())

    bairros_alerta = []
    for bairro in bairros:
        altitude_bairro_info = agente_altitude_bairro(bairro, cidade_alvo)
        pontos_bairro = [p for p in pontos_criticos_info if bairro in p["bairro"]]
        tipos_alagamento = list({p["tipo_alagamento"] for p in pontos_bairro})
        alerta_completo = agente_analise_risco_alagamento(
            bairro=bairro,
            cidade=cidade_alvo,
            previsao_chuva=previsao_chuva_info,
            tabua_mare=tabua_mare_info,
            lista_pontos_criticos=pontos_criticos_info,
            altitude_bairro=altitude_bairro_info
        )
        if "Justificativa:" in alerta_completo:
            alerta_final, justificativa = alerta_completo.split("Justificativa:", 1)
            alerta_final = alerta_final.strip()
            justificativa = justificativa.strip()
        else:
            alerta_final = alerta_completo
            justificativa = ""
        bairros_alerta.append({
            "bairro": bairro,
            "alerta_final": alerta_final,
            "justificativa": justificativa,
            "tipos_alagamento": tipos_alagamento
        })

    bairros_justificativas = {b["bairro"]: b["justificativa"] for b in bairros_alerta}

    return render_template(
        "home.html",
        bairros_alerta=bairros_alerta,
        previsao_chuva_info=previsao_chuva_info,
        tabua_mare_info=tabua_mare_info,
        pontos_criticos_info=pontos_criticos_info,
        bairros_coords=BAIRROS_COORDS,
        bairros_justificativas=bairros_justificativas
    )

@app.route("/relatar", methods=["GET", "POST"])
def relatar():
    if request.method == "POST":
        flash("Relato enviado! Obrigado por colaborar.", "success")
        return redirect(url_for("relatar"))
    return render_template("relatar.html")

@app.route("/alerta", methods=["POST"])
def alerta():
    flash("Inscrição simulada! Você receberá alertas de chuva e alagamento.", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
