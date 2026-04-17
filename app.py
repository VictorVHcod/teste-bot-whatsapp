from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

ZAPI_URL = "https://api.z-api.io/instances/3F1B93ED5CDD8251D0D10E5C90DD1B0B/token/65FB9421040863A98C3B5FAE/send-text"
ZAPI_TOKEN = "65FB9421040863A98C3B5FAE"
CLIENT_TOKEN = "Fbf300264fc57429db4b41a1a868b3249S"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json


    if not data or data.get("fromMe") is True:
        return jsonify({"status": "ignorado", "reason": "mensagem_do_proprio_bot"}), 200


    if data.get("isGroup") is True:
        return jsonify({"status": "ignorado", "reason": "mensagem_de_grupo"}), 200

    print("🔥 RECEBIDO:", data, flush=True)


    text_data = data.get("text", {})
    mensagem = ""
    if isinstance(text_data, dict):
        mensagem = text_data.get("message", "")
    elif isinstance(data.get("value"), str):
        mensagem = data.get("value")

    mensagem = str(mensagem).strip().lower()
    telefone = data.get("phone")


    if not mensagem or not telefone:
        return jsonify({"status": "ignorado", "reason": "dados_incompletos"}), 200

    telefone_limpo = str(telefone).split("@")[0]


    if "oi" in mensagem:
        resposta = "Oi! Tudo bem? Como posso te ajudar?\n\n[1] - Agendamento\n[2] - Dúvida"
    elif mensagem == "1":
        resposta = "Qual data você deseja agendar?"
    elif mensagem == "2":
        resposta = "É apenas um estudo de programador, TMJ 😄"
    else:

        resposta = "Não entendi 😅 Responda:\n[1] Agendamento\n[2] Dúvida"

    #
    try:
        headers = {
            "Content-Type": "application/json",
            "Client-Token": CLIENT_TOKEN
        }

        payload = {
            "phone": telefone_limpo,
            "message": resposta
        }

        print(f"Enviando resposta para {telefone_limpo}...", flush=True)
        response = requests.post(ZAPI_URL, json=payload, headers=headers)
        print(f"Status Z-API: {response.status_code} - {response.text}", flush=True)

    except Exception as e:
        print(f"❌ Erro no envio: {e}", flush=True)


    return jsonify({"status": "sucesso"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


