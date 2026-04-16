from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)


ZAPI_URL = "https://api.z-api.io/instances/3F1B93ED5CDD8251D0D10E5C90DD1B0B/token/65FB9421040863A98C3B5FAE/send-text"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    print("🔥 RECEBIDO:", data)


    mensagem = ""
    if data:
        mensagem = (
            data.get("message")
            or data.get("body")
            or (data.get("text") or {}).get("message")
            or ""
        ).strip().lower()

    telefone = data.get("phone") if data else None

    print("📩 MENSAGEM:", mensagem)
    print("📞 TELEFONE:", telefone)


    if "oi" in mensagem:
        resposta = "Oi! Tudo bem? Como posso te ajudar?\n\n[1] - Agendamento\n[2] - Dúvida"

    elif mensagem == "1":
        resposta = "Qual data você deseja agendar?"

    elif mensagem == "2":
        resposta = "É apenas um estudo de programador, TMJ 😄"

    else:
        resposta = "Não entendi 😅 Responda:\n[1] Agendamento\n[2] Dúvida"

    if telefone:
        try:
            requests.post(ZAPI_URL, json={
                "phone": telefone,
                "message": resposta
            })

            print("✅ Mensagem enviada com sucesso")

        except Exception as e:
            print("❌ Erro ao enviar mensagem:", e)

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )


