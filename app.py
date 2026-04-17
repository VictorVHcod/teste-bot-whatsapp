from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)


ZAPI_URL = "https://api.z-api.io/instances/3F1B93ED5CDD8251D0D10E5C90DD1B0B/token/65FB9421040863A98C3B5FAE/send-text"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("🔥 RECEBIDO:", data,flush=True)


    mensagem = ""
    if data:
        text_data = data.get("text", {})
        mensagem = (
                data.get("message")
                or data.get("body")
                or (text_data.get("message") if isinstance(text_data, dict) else None)
                or ""
        ).strip().lower()

    telefone = data.get("phone") or data.get("sender")

    print(f"📩 MENSAGEM: {mensagem} | 📞 TELEFONE: {telefone}",flush=True)

    if "oi" in mensagem:

        resposta = "Oi! Tudo bem? Como posso te ajudar?\n\n[1] - Agendamento\n[2] - Dúvida"



    elif mensagem == "1":

        resposta = "Qual data você deseja agendar?"



    elif mensagem == "2":

        resposta = "É apenas um estudo de programador, TMJ 😄"



    else:

        resposta = "Não entendi 😅 Responda:\n[1] Agendamento\n[2] Dúvida"


    if telefone:

        telefone_limpo = str(telefone).split("@")[0]


        if "-" in telefone_limpo:
            print(f"Ignorando grupo: {telefone_limpo}", flush=True)
            return jsonify({"status": "ok"})

        try:
            print(f"Enviando resposta para {telefone_limpo}...", flush=True)


            token_seguranca = "65FB9421040863A98C3B5FAE"


            headers = {
                "Content-Type": "application/json",
                "Client-Token": token_seguranca
            }


            response = requests.post(
                ZAPI_URL,
                json={
                    "phone": telefone_limpo,
                    "message": resposta
                },
                headers=headers  # <--- ESSA É A CHAVE!
            )

            print(f"Status Z-API: {response.status_code} - {response.text}", flush=True)

        except Exception as e:
            print("❌ Erro ao enviar mensagem:", e, flush=True)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )


