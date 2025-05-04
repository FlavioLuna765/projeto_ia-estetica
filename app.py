from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def responder_pergunta(pergunta):
    pergunta = pergunta.lower()
    if "serviços" in pergunta:
        return "Oferecemos: limpeza de pele, depilação, manicure, pedicure, design de sobrancelhas, e massagens."
    elif "limpeza de pele" in pergunta or "valor" in pergunta:
        return "A limpeza de pele custa R$120,00 e dura cerca de 1h."
    elif "agendar" in pergunta or "marcar" in pergunta:
        return "Você pode agendar pelo WhatsApp (99) 99999-9999 ou direto em nosso site."
    elif "funcionamento" in pergunta or "horário" in pergunta:
        return "Funcionamos de segunda a sábado, das 9h às 19h."
    elif "localização" in pergunta:
        return "Estamos localizados na Rua das Flores, nº 123 – Centro."
    else:
        return "Desculpe, não entendi. Tente perguntar sobre serviços, valores ou horários."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/mensagem', methods=['POST'])
def mensagem():
    data = request.json
    pergunta = data.get('pergunta', '')
    resposta = responder_pergunta(pergunta)
    return jsonify({'resposta': resposta})


if __name__ == '__main__':
    app.run(debug=True)
