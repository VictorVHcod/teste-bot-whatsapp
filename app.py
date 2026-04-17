from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

ZAPI_URL = "https://api.z-api.io/instances/3F1B93ED5CDD8251D0D10E5C90DD1B0B/token/65FB9421040863A98C3B5FAE/send-text"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("🔥 RECEBIDO:", data, flush=True)

    if not data:
        return jsonify({"status": "no data"}), 200


    text_data = data.get("text", {})
    mensagem = (
            data.get("message")
            or data.get("body")
            or (text_data.get("message") if isinstance(text_data, dict) else None)
            or ""
    ).strip().lower()


    telefone = data.get("phone") or data.get("sender")

    if not telefone:
        return jsonify({"status": "no phone"}), 200

    telefone_limpo = str(telefone).split("@")[0]
    print(f"📩 MENSAGEM: {mensagem} | 📞 TELEFONE: {telefone_limpo}", flush=True)


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
            "Client-Token": "65FB9421040863A98C3B5FAE"
        }

        payload = {
            "phone": telefone_limpo,
            "message": resposta
        }

        print(f"Enviando para Z-API...", flush=True)
        response = requests.post(ZAPI_URL, json=payload, headers=headers)
        print(f"Status Z-API: {response.status_code} - {response.text}", flush=True)

    except Exception as e:
        print("❌ Erro no requests:", e, flush=True)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


