from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)


ZAPI_URL = "https://api.z-api.io/instances/3F1B93ED5CDD8251D0D10E5C90DD1B0B/token/65FB9421040863A98C3B5FAE/send-text"
ZAPI_TOKEN = "65FB9421040863A98C3B5FAE"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("🔥 RECEBIDO:", data, flush=True)

    if not data:
        return jsonify({"status": "sem dados"}), 200


    text_data = data.get("text", {})
    mensagem = (data.get("message") or data.get("body") or (
        text_data.get("message") if isinstance(text_data, dict) else "") or "").strip().lower()
    telefone = data.get("phone") or data.get("sender")

    if not telefone:
        return jsonify({"status": "sem telefone"}), 200

    telefone_limpo = str(telefone).split("@")[0]


    if "oi" in mensagem:
        resposta = "Oi! Tudo bem? Como posso te ajudar?\n\n[1] - Agendamento\n[2] - Dúvida"
    elif mensagem == "1":
        resposta = "Qual data você deseja agendar?"
    elif mensagem == "2":
        resposta = "É apenas um estudo de programador, TMJ 😄"
    else:
        resposta = "Não entendi 😅 Responda:\n[1] Agendamento\n[2] Dúvida"

    try:

        headers = {
            "Content-Type": "application/json",
            "client-token": ZAPI_TOKEN,
            "Client-Token": ZAPI_TOKEN
        }

        payload = {
            "phone": telefone_limpo,
            "message": resposta
        }

        print(f"Tentando enviar para {telefone_limpo}...", flush=True)


        URL_ENVIO = f"https://api.z-api.io/instances/3F1B93ED5CDD8251D0D10E5C90DD1B0B/token/{ZAPI_TOKEN}/send-text"

        response = requests.post(URL_ENVIO, json=payload, headers=headers)
        print(f"Status Z-API: {response.status_code} - {response.text}", flush=True)

    except Exception as e:
        print(f"❌ Erro na requisição: {e}", flush=True)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


