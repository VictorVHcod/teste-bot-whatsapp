from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    mensagem = data.get("text", {}).get("message", "") or ""
    mensagem = mensagem.lower()
    telefone = data.get("phone")

    if "oi" in mensagem:
        resposta = """
        Oi! Tudo bem? Como posso te ajudar ?

        [1] - Agendamento
        [2] - dúvida

        """
    elif mensagem == "1":
        resposta = "Qual data deseja agendar?"
    elif mensagem == "2":
        resposta = "É apenas um estudo de programador, TMJ"
    else:
        return {"status": "ok"}

    return jsonify({
        "phone": telefone,
        "message": resposta
    })

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))


