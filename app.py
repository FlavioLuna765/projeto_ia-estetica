from flask import Flask, render_template, request, jsonify, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'chave-secreta-para-chat'
app.permanent_session_lifetime = timedelta(minutes=10)

agendamentos = {}

def responder_pergunta(pergunta):
    pergunta = pergunta.lower()
    session.permanent = True

    if 'etapa_agendamento' not in session:
        session['etapa_agendamento'] = None
        session['dados_agendamento'] = {}

    etapa = session['etapa_agendamento']
    dados = session['dados_agendamento']

    if "agendar" in pergunta or "marcar" in pergunta or etapa:
        if not etapa:
            session['etapa_agendamento'] = 'nome'
            return "Claro! Vamos agendar seu atendimento. Qual é o seu nome completo?"

        elif etapa == 'nome':
            dados['nome'] = pergunta.title()
            session['etapa_agendamento'] = 'serviço'
            return f"Obrigada, {dados['nome']}! Qual serviço você deseja agendar?"

        elif etapa == 'serviço':
            dados['serviço'] = pergunta
            session['etapa_agendamento'] = 'data'
            return "Perfeito! Qual dia você gostaria de agendar? (Ex: 15/05)"

        elif etapa == 'data':
            dados['data'] = pergunta
            session['etapa_agendamento'] = 'hora'
            return "E qual horário você prefere? (Ex: 14h ou 14:00)"

        elif etapa == 'hora':
            dados['hora'] = pergunta
            session['etapa_agendamento'] = None
            cliente = dados['nome']
            servico = dados['serviço']
            data_hora = f"{dados['data']} às {dados['hora']}"

            agendamentos[cliente] = {
                'serviço': servico,
                'data': dados['data'],
                'hora': dados['hora']
            }

            session['dados_agendamento'] = {}

            return (
                f"✅ Agendamento concluído!\n"
                f"Cliente: {cliente}\n"
                f"Serviço: {servico}\n"
                f"Data e Hora: {data_hora}\n\n"
                f"Você precisa de mais alguma coisa? (Sim/Não)"
            )

    # Respostas melhoradas com palavras-chave flexíveis
    if any(p in pergunta for p in ["serviços", "procedimentos", "o que vocês fazem"]):
        return (
            "Oferecemos os seguintes serviços:\n"
            "- Design de sobrancelha\n"
            "- Micropigmentação de sobrancelha\n"
            "- Micropigmentação de lábios\n"
            "- Depilação geral com cera\n"
            "- Limpeza profunda de pele com microagulhamento\n"
            "- Tratamento facial com jato de plasma\n"
            "- Peeling de algas\n"
            "- Dermaplaning"
        )

    elif any(p in pergunta for p in ["sobrancelha", "design de sobrancelha", "fazer sobrancelha"]):
        return (
            "O design de sobrancelha valoriza seu olhar com técnicas de simetria facial. "
            "Dura cerca de 30 minutos e custa R$40,00."
        )

    elif any(p in pergunta for p in ["micropigmentação"]):
        return (
            "Temos dois tipos de micropigmentação:\n"
            "- Micropigmentação de sobrancelhas\n"
            "- Micropigmentação de lábios\n"
            "Qual deles você gostaria de saber mais?"
        )

    elif any(p in pergunta for p in ["micropigmentação de sobrancelha", "fio a fio", "micropigmentar sobrancelha", "micropigmentacao sobrancelha"]):
        return (
            "A micropigmentação de sobrancelhas simula fios para corrigir falhas. "
            "Dura de 1 a 2 anos e custa R$350,00."
        )

    elif any(p in pergunta for p in ["micropigmentação de lábios", "micropigmentação labial", "lábios", "pigmentar boca"]):
        return (
            "Realça o contorno e a cor dos lábios, com efeito natural. "
            "Custa R$400,00 e dura cerca de 2 horas."
        )

    elif any(p in pergunta for p in ["depilação", "depilar", "cera", "pelos"]):
        return (
            "Fazemos depilação com cera quente para todo o corpo. "
            "Preços entre R$30 e R$100 conforme a área."
        )

    elif any(p in pergunta for p in ["limpeza", "limpeza de pele", "microagulhamento", "limpar rosto", "cravos"]):
        return (
            "A limpeza profunda com microagulhamento remove impurezas e estimula colágeno. "
            "Ideal para peles com acne ou manchas. Valor: R$180,00."
        )

    elif any(p in pergunta for p in ["jato de plasma", "plasma", "manchas", "tratamento facial plasma"]):
        return (
            "O jato de plasma é usado para rejuvenescimento e remoção de manchas. "
            "Valor: R$250,00 por sessão."
        )

    elif any(p in pergunta for p in ["peeling", "peeling de algas", "algas", "esfoliação"]):
        return (
            "O peeling de algas é natural e indicado para peles sensíveis. "
            "Promove renovação celular. Valor: R$150,00."
        )

    elif any(p in pergunta for p in ["dermaplaning", "dermaplanagem", "pelos faciais", "raspar pele"]):
        return (
            "O dermaplaning remove células mortas e pelos finos do rosto. Deixa a pele lisa e brilhante. "
            "Valor: R$130,00."
        )

    elif any(p in pergunta for p in ["dói", "dói muito", "é dolorido", "machuca"]):
        return "Os procedimentos são feitos com muito cuidado. A maioria é bem tolerável e pouco dolorida."

    elif any(p in pergunta for p in ["quantas sessões", "quantas vezes", "precisa de mais de uma"]):
        return "Depende do tratamento e do tipo de pele. Normalmente são de 1 a 4 sessões."

    elif any(p in pergunta for p in ["duração", "quanto tempo", "demora"]):
        return "Os procedimentos duram entre 30 minutos e 2 horas, dependendo do tipo."

    elif any(p in pergunta for p in ["horário", "funcionamento", "abre que horas", "fecha que horas"]):
        return "Funcionamos de segunda a sábado, das 9h às 19h."

    elif any(p in pergunta for p in ["localização", "onde fica", "endereço", "como chegar"]):
        return "Estamos localizados na Rua das Flores, nº 123 – Centro."

    elif any(p in pergunta for p in ["não", "não precisa", "não quero mais nada", "nada"]):
        return "Muito obrigado pelo seu tempo! 😊 Ficamos à disposição para tirar mais dúvidas ou agendar novos serviços. Até logo!"

    return "Desculpe, não entendi. Você pode perguntar sobre serviços, valores ou agendamento."


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
