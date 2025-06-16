from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'segredo-super-seguro'

LINHAS = ['A', 'B', 'C', 'D', 'E']
COLUNAS = ['1', '2', '3', '4', '5']

PALAVRAS_FORCA = [
    'Roblox', 'Pokemon', 'Minecraft', 'Super Mario', 'The last of us', 'Sonic',
    'Free Fire', 'Genshin Impact', 'Apex Legends', 'Grand Theft Auto', 'Red Dead Redemption',
    'The Witcher', 'Overwatch', 'Tetris', 'Halo', 'Call of Duty', 'Fifa', 'League of Legends',
    'Dota', 'Phasmophobia', 'Fortnite', 'Rocket League', 'Tomb Raider', 'Paladins', 'Brawl Stars'
]

QUIZ_PERGUNTAS = [
    {
        "pergunta": "Quem foi a primeira protagonista feminina nos jogos?",
        "opcoes": [
            "Lara Croft em Tomb Raider",
            "Ellie de The Last of Us parte 2",
            "Jill Valentine em Resident Evil 3",
            "Ms Pacman da franquia de Pacman"
        ],
        "resposta_correta": 4,
        "pontos": 1
    },
    {
        "pergunta": "Quem desses NÃO foi um ator do Batman?",
        "opcoes": [
            "Ben Affleck",
            "Daniel Craig",
            "Michael Keaton",
            "Gus Lewis"
        ],
        "resposta_correta": 2,
        "pontos": 2
    },
    {
        "pergunta": "Quem foi o primeiro campeão mundial de Pokemon World Championship?",
        "opcoes": [
            "Park Se-jun",
            "Piter Bryon",
            "Akira Toriyama",
            "Yoo-Joonghyuk"
        ],
        "resposta_correta": 1,
        "pontos": 3
    },
    {
        "pergunta": "Qual dessas afirmações sobre o personagem The Radiance é verdadeira?",
        "opcoes": [
            "The Radiance é a forma corrompida do Hollow Knight original.",
            "The Radiance é uma entidade benevolente que guia os habitantes de Hallownest.",
            "The Radiance é um ser de luz esquecido, responsável pela infecção mental dos insetos.",
            "The Radiance era originalmente o pai do Hollow"
        ],
        "resposta_correta": 3,
        "pontos": 2
    },
    {
        "pergunta": "Black Dahlia é uma assassina cruel e boa de briga. Qual é a arma mais icônica dela durante o combate?",
        "opcoes": [
            "Um chicote envenenado com veneno de Skullgirl",
            "Lâminas ocultas nos braços",
            "Um rifle-escopeta com munições especiais",
            "Guarda-chuva que dispara ácido"
        ],
        "resposta_correta": 3,
        "pontos": 1
    },
    {
        "pergunta": "Qual anime NÃO foi classificado como melhor anime do ano no Anime Awards 2025?",
        "opcoes": [
            "Dan Da Dan",
            "Frieren e a Jornada para o além",
            "Solo Leveling",
            "Demon Slayer - Arco do Castelo Infinito"
        ],
        "resposta_correta": 4,
        "pontos": 1
    }
]

NUM_DISCOS = 4
HASTES = ['A', 'B', 'C']

def inicializar_torre_hanoi():
    # Discos do maior (NUM_DISCOS) para o menor (1)
    discos_base = list(range(NUM_DISCOS, 0, -1))
    
    session["hanoi_game"] = {
        'A': discos_base,
        'B': [],
        'C': []
    }
    session["hanoi_movimentos"] = 0
    session["hanoi_mensagem"] = "Bem-vindo à Torre de Hanói! Mova os discos de A para C."
    session["hanoi_vitoria"] = False

def validar_movimento_hanoi(origem_haste, destino_haste):
    hastes = session["hanoi_game"]

    if origem_haste not in HASTES or destino_haste not in HASTES:
        return "Haste de origem ou destino inválida. Escolha A, B ou C."

    if origem_haste == destino_haste:
        return "As hastes de origem e destino devem ser diferentes."

    if not hastes[origem_haste]:
        return f"A haste '{origem_haste}' está vazia. Não há discos para mover."

    disco_origem = hastes[origem_haste][-1]

    if not hastes[destino_haste] or disco_origem < hastes[destino_haste][-1]:
        return None
    else:
        disco_destino = hastes[destino_haste][-1]
        return f"Movimento inválido! Disco {disco_origem} não pode ser colocado sobre o disco {disco_destino}."

def executar_movimento_hanoi(origem_haste, destino_haste):
    hastes = session["hanoi_game"]
    disco = hastes[origem_haste].pop()
    hastes[destino_haste].append(disco)
    session["hanoi_movimentos"] += 1
    session["hanoi_game"] = hastes

def verificar_vitoria_hanoi():
    hastes = session["hanoi_game"]
    # Condição de vitória: discos do maior para o menor (igual ao inicial)
    condicao_vitoria = list(range(NUM_DISCOS, 0, -1))
    return hastes['C'] == condicao_vitoria

@app.route("/")
def index():
    jogos = [
        {"nome": "Adivinhe o número", "rota": "adivinhe"},
        {"nome": "Batalha Naval", "rota": "batalha_naval"},
        {"nome": "Forca", "rota": "forca"},
        {"nome": "Pedra, Papel e Tesoura", "rota": "pedra_papel_tesoura"},
        {"nome": "Quiz Geek", "rota": "quiz"},
        {"nome": "Torre de Hanói", "rota": "torre_hanoi"}
    ]
    return render_template("index.html", jogos=jogos)

@app.route("/adivinhe", methods=["GET", "POST"])
def adivinhe():
    if 'numero_secreto' not in session:
        session['numero_secreto'] = random.randint(1, 100)

    resultado = None

    if request.method == "POST":
        try:
            palpite = int(request.form["palpite"])
            numero_secreto = session['numero_secreto']

            if palpite < numero_secreto:
                resultado = "Tente um número maior!"
            elif palpite > numero_secreto:
                resultado = "Tente um número menor!"
            else:
                resultado = "Parabéns! Você acertou! Um novo número foi sorteado."
                session['numero_secreto'] = random.randint(1, 100)
        except ValueError:
            resultado = "Digite um número válido."

    return render_template("adivinhe.html", resultado=resultado)

@app.route("/batalha_naval", methods=["GET", "POST"])
def batalha_naval():
    if "navio_posicao" not in session or "tentativas" not in session:
        session["navio_posicao"] = (random.choice(LINHAS), random.choice(COLUNAS))
        session["tentativas"] = 5
        session["resultado"] = None
        session["jogo_finalizado"] = False

    resultado = session["resultado"]
    tentativas_restantes = session["tentativas"]
    jogo_finalizado = session["jogo_finalizado"]

    if request.method == "POST" and not jogo_finalizado:
        linha_chute = request.form.get("linha")
        coluna_chute = request.form.get("coluna")

        if linha_chute not in LINHAS or coluna_chute not in COLUNAS:
            session["resultado"] = "Por favor, escolha uma linha entre A-E e uma coluna entre 1-5."
        else:
            navio_linha, navio_coluna = session["navio_posicao"]

            if linha_chute == navio_linha and coluna_chute == navio_coluna:
                session["resultado"] = f"Você acertou o navio na posição {linha_chute}{coluna_chute}! Vitória!"
                session["jogo_finalizado"] = True
            else:
                session["tentativas"] -= 1
                if session["tentativas"] > 0:
                    session["resultado"] = f"Você errou! Tentou a posição {linha_chute}{coluna_chute}. Tentativas restantes: {session['tentativas']}."
                else:
                    session["resultado"] = f"Fim de jogo! Você errou sua última tentativa. O navio estava na posição {navio_linha}{navio_coluna}."
                    session["jogo_finalizado"] = True
        
        resultado = session["resultado"]
        tentativas_restantes = session["tentativas"]
        jogo_finalizado = session["jogo_finalizado"]

    return render_template(
        "batalha_naval.html",
        resultado=resultado,
        tentativas_restantes=tentativas_restantes,
        jogo_finalizado=jogo_finalizado
    )

@app.route("/reiniciar_jogo")
def reiniciar_jogo():
    session.pop("navio_posicao", None)
    session.pop("tentativas", None)
    session.pop("resultado", None)
    session.pop("jogo_finalizado", None)
    return redirect(url_for("batalha_naval"))

@app.route("/forca", methods=["GET", "POST"])
def forca():
    if "palavra_secreta" not in session or "jogo_forca_finalizado" not in session:
        palavra_random = random.choice(PALAVRAS_FORCA).upper()
        session["palavra_secreta"] = palavra_random
        session["letras_descobertas"] = [' ' if letra == ' ' else '_' for letra in palavra_random]
        session["erros"] = 0
        session["chutes"] = []
        session["resultado_forca"] = None
        session["jogo_forca_finalizado"] = False
        session["mensagem_final"] = None
    
    resultado_forca = session["resultado_forca"]
    palavra_exibida = "".join(session["letras_descobertas"]) 
    erros_atuais = session["erros"]
    chutes_feitos = sorted(session["chutes"])
    jogo_forca_finalizado = session["jogo_forca_finalizado"]
    mensagem_final = session["mensagem_final"]
    
    if request.method == "POST" and not jogo_forca_finalizado:
        tentativa = request.form.get("letra", "").upper().strip()

        if not tentativa.isalpha() or len(tentativa) != 1:
            session["resultado_forca"] = "Por favor, digite apenas uma letra válida."
        elif tentativa in session["chutes"]:
            session["resultado_forca"] = f"Você já tentou a letra '{tentativa}'."
        else:
            session["chutes"].append(tentativa)
            palavra_secreta = session["palavra_secreta"]
            letras_descobertas = session["letras_descobertas"]
            
            if tentativa in palavra_secreta:
                session["resultado_forca"] = f"A letra '{tentativa}' está na palavra!"
                for i in range(len(palavra_secreta)):
                    if palavra_secreta[i] == tentativa:
                        letras_descobertas[i] = tentativa
                session["letras_descobertas"] = letras_descobertas
            else:
                session["resultado_forca"] = f"A letra '{tentativa}' não está na palavra."
                session["erros"] += 1

            if "_" not in session["letras_descobertas"]:
                session["resultado_forca"] = "Parabéns! Você descobriu a palavra!"
                session["mensagem_final"] = f"Parabéns! Você descobriu! O jogo é: '{palavra_secreta}'"
                session["jogo_forca_finalizado"] = True
            elif session["erros"] >= 6:
                session["resultado_forca"] = "Você perdeu! Fim de jogo."
                session["mensagem_final"] = f"Que pena! Você foi enforcado. A palavra era: '{palavra_secreta}'."
                session["jogo_forca_finalizado"] = True
            
        resultado_forca = session["resultado_forca"]
        palavra_exibida = "".join(session["letras_descobertas"]) 
        erros_atuais = session["erros"]
        chutes_feitos = sorted(session["chutes"])
        jogo_forca_finalizado = session["jogo_forca_finalizado"]
        mensagem_final = session["mensagem_final"]

    return render_template(
        "forca.html",
        palavra_exibida=palavra_exibida,
        erros=erros_atuais,
        chutes_feitos=", ".join(chutes_feitos),
        resultado_forca=resultado_forca,
        jogo_forca_finalizado=jogo_forca_finalizado,
        mensagem_final=mensagem_final
    )

@app.route("/reiniciar_forca")
def reiniciar_forca():
    session.pop("palavra_secreta", None)
    session.pop("letras_descobertas", None)
    session.pop("erros", None)
    session.pop("chutes", None)
    session.pop("resultado_forca", None)
    session.pop("jogo_forca_finalizado", None)
    session.pop("mensagem_final", None)
    return redirect(url_for("forca"))

@app.route("/pedra_papel_tesoura", methods=["GET", "POST"])
def pedra_papel_tesoura():
    opcoes = ["PEDRA", "PAPEL", "TESOURA"]
    
    if "ppt_placar_usuario" not in session:
        session["ppt_placar_usuario"] = 0
        session["ppt_placar_computador"] = 0
        session["ppt_escolha_usuario"] = None
        session["ppt_escolha_computador"] = None
        session["ppt_resultado_rodada"] = None

    escolha_usuario = None
    resultado_rodada = None

    if request.method == "POST":
        escolha_usuario = request.form.get("escolha").upper()
        if escolha_usuario in opcoes:
            escolha_computador = random.choice(opcoes)
            session["ppt_escolha_usuario"] = escolha_usuario
            session["ppt_escolha_computador"] = escolha_computador

            if escolha_usuario == escolha_computador:
                resultado_rodada = "Empate!"
            elif (escolha_usuario == "PEDRA" and escolha_computador == "TESOURA") or \
                 (escolha_usuario == "PAPEL" and escolha_computador == "PEDRA") or \
                 (escolha_usuario == "TESOURA" and escolha_computador == "PAPEL"):
                resultado_rodada = "Você venceu!"
                session["ppt_placar_usuario"] += 1
            else:
                resultado_rodada = "O computador venceu!"
                session["ppt_placar_computador"] += 1
            
            session["ppt_resultado_rodada"] = resultado_rodada
        else:
            session["ppt_resultado_rodada"] = "Opção inválida!"

    return render_template(
        "pedra_papel_tesoura.html",
        placar_usuario=session["ppt_placar_usuario"],
        placar_computador=session["ppt_placar_computador"],
        escolha_usuario=session["ppt_escolha_usuario"],
        escolha_computador=session["ppt_escolha_computador"],
        resultado_rodada=session["ppt_resultado_rodada"]
    )

@app.route("/reiniciar_ppt")
def reiniciar_ppt():
    session.pop("ppt_placar_usuario", None)
    session.pop("ppt_placar_computador", None)
    session.pop("ppt_escolha_usuario", None)
    session.pop("ppt_escolha_computador", None)
    session.pop("ppt_resultado_rodada", None)
    return redirect(url_for("pedra_papel_tesoura"))


@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if "quiz_pontuacao" not in session:
        session["quiz_pontuacao"] = 0
        session["quiz_pergunta_atual"] = 0
        session["quiz_resultado_rodada"] = None
        session["quiz_terminado"] = False

    if request.method == "POST" and not session["quiz_terminado"]:
        resposta_usuario = request.form.get("resposta_quiz", type=int)
        pergunta_atual_idx = session["quiz_pergunta_atual"]
        
        if pergunta_atual_idx < len(QUIZ_PERGUNTAS):
            pergunta_obj = QUIZ_PERGUNTAS[pergunta_atual_idx]
            
            if resposta_usuario == pergunta_obj["resposta_correta"]:
                session["quiz_pontuacao"] += pergunta_obj["pontos"]
                session["quiz_resultado_rodada"] = "correta"
            else:
                session["quiz_resultado_rodada"] = "errada"
            
            session["quiz_pergunta_atual"] += 1
            
            if session["quiz_pergunta_atual"] >= len(QUIZ_PERGUNTAS):
                session["quiz_terminado"] = True
    
    current_question = None
    if not session["quiz_terminado"]:
        current_question_index = session["quiz_pergunta_atual"]
        if current_question_index < len(QUIZ_PERGUNTAS):
            current_question = QUIZ_PERGUNTAS[current_question_index]
        else:
            session["quiz_terminado"] = True

    return render_template(
        "quiz.html",
        pergunta=current_question,
        pontuacao=session["quiz_pontuacao"],
        quiz_terminado=session["quiz_terminado"],
        resultado_rodada=session["quiz_resultado_rodada"],
        total_perguntas=len(QUIZ_PERGUNTAS)
    )

@app.route("/reiniciar_quiz")
def reiniciar_quiz():
    session.pop("quiz_pontuacao", None)
    session.pop("quiz_pergunta_atual", None)
    session.pop("quiz_resultado_rodada", None)
    session.pop("quiz_terminado", None)
    return redirect(url_for("quiz"))


@app.route("/torre_hanoi", methods=["GET", "POST"])
def torre_hanoi():
    if "hanoi_game" not in session or not isinstance(session["hanoi_game"], dict) or \
       any(haste_name not in session["hanoi_game"] for haste_name in HASTES):
        inicializar_torre_hanoi()

    game_state = session["hanoi_game"]
    movimentos = session["hanoi_movimentos"]
    mensagem = session["hanoi_mensagem"]
    vitoria = session["hanoi_vitoria"]

    if request.method == "POST" and not vitoria:
        origem = request.form.get("origem").upper()
        destino = request.form.get("destino").upper()

        erro = validar_movimento_hanoi(origem, destino)

        if erro:
            session["hanoi_mensagem"] = erro
        else:
            executar_movimento_hanoi(origem, destino)
            session["hanoi_mensagem"] = "Movimento realizado com sucesso!"
            
            if verificar_vitoria_hanoi():
                session["hanoi_vitoria"] = True
                min_movimentos = (2**NUM_DISCOS) - 1
                session["hanoi_mensagem"] = (
                    f"Parabéns! Você resolveu a Torre de Hanói em {session['hanoi_movimentos']} movimentos! "
                    f"O mínimo de movimentos para {NUM_DISCOS} discos é: {min_movimentos}"
                )

    return render_template(
        "torre_hanoi.html",
        hastes=session["hanoi_game"],
        num_discos=NUM_DISCOS,
        movimentos=session["hanoi_movimentos"],
        mensagem=session["hanoi_mensagem"],
        vitoria=session["hanoi_vitoria"],
        hastes_nomes=HASTES
    )

@app.route("/reiniciar_hanoi")
def reiniciar_hanoi():
    session.pop("hanoi_game", None)
    session.pop("hanoi_movimentos", None)
    session.pop("hanoi_mensagem", None)
    session.pop("hanoi_vitoria", None)
    return redirect(url_for("torre_hanoi"))


if __name__ == "__main__":
    app.run(debug=True)