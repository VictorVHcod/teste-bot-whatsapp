from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)


ZAPI_URL = "https://api.z-api.io/instances/3F1B93ED5CDD8251D0D10E5C90DD1B0B/token/65FB9421040863A98C3B5FAE/send-text"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("🔥 RECEBIDO:", data)

    # Captura a mensagem de diferentes estruturas possíveis da Z-API
    mensagem = ""
    if data:
        text_data = data.get("text", {})
        mensagem = (
                data.get("message")
                or data.get("body")
                or (text_data.get("message") if isinstance(text_data, dict) else None)
                or ""
        ).strip().lower()

    # Tenta pegar o telefone de 'phone' ou 'sender' (padrão Z-API)
    telefone = data.get("phone") or data.get("sender")

    print(f"📩 MENSAGEM: {mensagem} | 📞 TELEFONE: {telefone}")

    if "oi" in mensagem:

        resposta = "Oi! Tudo bem? Como posso te ajudar?\n\n[1] - Agendamento\n[2] - Dúvida"



    elif mensagem == "1":

        resposta = "Qual data você deseja agendar?"



    elif mensagem == "2":

        resposta = "É apenas um estudo de programador, TMJ 😄"



    else:

        resposta = "Não entendi 😅 Responda:\n[1] Agendamento\n[2] Dúvida"

    if telefone:
        # Garante que o telefone está no formato string e sem @c.us se existir
        telefone = str(telefone).split("@")[0]

        try:
            # Tente imprimir o que está enviando para debugar
            print(f"Enviando resposta para {telefone}...")

            response = requests.post(ZAPI_URL, json={
                "phone": telefone,
                "message": resposta
            })

            print(f"Status Z-API: {response.status_code} - {response.text}")

        except Exception as e:
            print("❌ Erro ao enviar mensagem:", e)

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )


