from flask import Flask, render_template, request, flash, redirect, url_for, session, make_response

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

usuarios_cadastrados = []
USUARIO_FIXO = {'username': 'teste', 'password': '123'}

NOTICIAS = [
    {'titulo': 'São Paulo vence clássico Majestoso e Mirassol atropela o Santos', 'categoria': 'Esportes', 'conteudo': 'O São Paulo venceu o clássico “Majestoso” por 2 × 0 em casa, enquanto o Mirassol goleou o Santos por 3 × 0 na mesma rodada'},
    {'titulo': 'Preta Gil morre aos 50 anos, nos Estados Unidos', 'categoria': 'Entretenimento', 'conteudo': 'A cantora Preta Gil faleceu em 20 de julho, aos 50 anos, após complicações de câncer nos EUA; a notícia foi confirmada por sua assessoria.'},
    {'titulo': 'Parque de SP terá o maior toboágua do planeta em 2026', 'categoria': 'Lazer', 'conteudo': 'O Acqua Thermas Park, em Sorocaba (90 km de SP), incluirá o maior toboágua e uma praia artificial de 3 000 m², inaugurando em 2026.'},
    {'titulo': 'Tati Dias lança campeonato de futevôlei apenas para mulheres em São Paulo', 'categoria': 'Esportes', 'conteudo': 'A influenciadora Tati Dias lançou o “Circuito Gaia de Futevôlei”, primeira competição 100 % feminina realizada num espaço na zona sul da capital.'},
    {'titulo': 'Governo de SP anuncia ações de incentivo a circos', 'categoria': 'Entretenimento', 'conteudo': 'O governo estadual lançou três novidades culturais: o Troféu Picadeiro, programa Pró‑Circo e o Festival de Circo SP 2025.'},
    {'titulo': 'Maior tirolesa do mundo terá 3,4 km e ficará no interior de São Paulo', 'categoria': 'Lazer', 'conteudo': 'Uma enorme tirolesa de 3,4 km será instalada no interior paulista, apontada como recorde mundial em extensão.'},
    {'titulo': 'Brasileirão retorna com Flamengo x São Paulo neste sábado no Maracanã', 'categoria': 'Esportes', 'conteudo': 'A partida entre Flamengo e São Paulo marcou o retorno do Brasileirão; apesar de não ocorrer em SP, envolve diretamente o time da cidade.'},
    {'titulo': 'Série de TV de sucesso renovada para nova temporada', 'categoria': 'Entretenimento', 'conteudo': 'Os fãs da série já podem comemorar a continuação da história que conquistou milhões de espectadores em todo o mundo.'},
    {'titulo': '🖼 Andy Warhol e o pop art brasileiro dialogam em São Paulo', 'categoria': 'Lazer', 'conteudo': 'Duas exposições na capital destacam o pop art: uma com 600 obras de Warhol na FAAP e outra com artistas brasileiros na Pinacoteca, com críticas sociais e políticas dos anos 60 e 70..'},
]

@app.context_processor
def inject_theme():

    return dict(current_theme=request.cookies.get('theme', 'claro')) 

@app.route('/registrarUsuario', methods=['GET', 'POST'])
def registrarUsuario():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash('Todos os campos são obrigatórios!', 'danger')
        elif not "@" in email or not "." in email:
            flash('Formato de e-mail inválido!', 'danger')
        elif len(password) < 6:
            flash('A senha deve ter pelo menos 6 caracteres!', 'danger')
        else:
            if any(u['username'] == username for u in usuarios_cadastrados):
                flash(f'O usuário "{username}" já existe. Por favor, escolha outro.', 'danger')
            else:
                usuarios_cadastrados.append({'username': username, 'email': email, 'password': password})
                flash(f'Usuário {username} cadastrado com sucesso! Agora você pode fazer login.', 'success')
                return redirect(url_for('login'))
    return render_template('formulario.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        usuario_encontrado = None
        for user in usuarios_cadastrados:
            if user['username'] == username and user['password'] == password:
                usuario_encontrado = user
                break

        if not usuario_encontrado and username == USUARIO_FIXO['username'] and password == USUARIO_FIXO['password']:
             usuario_encontrado = USUARIO_FIXO

        if usuario_encontrado:
            session['username'] = username
            session['views'] = 0 
            flash(f'Bem-vindo, {username}!', 'success')
            return redirect(url_for('boas_vindas')) 
        else:
            flash('Nome de usuário ou senha inválidos.', 'danger')
    return render_template('login.html')



@app.route('/boas_vindas')
def boas_vindas():

    if 'username' not in session:
        flash('Você precisa fazer login para acessar esta página.', 'danger')
        return redirect(url_for('login'))

    username = session['username']
    session['views'] = session.get('views', 0) + 1 
    views_count = session['views']

    return render_template('boas_vindas.html', username=username, views_count=views_count)


@app.route('/set_theme/<theme>')
def set_theme(theme):
    if theme in ['claro', 'escuro']:
        response = make_response(redirect(request.referrer or url_for('boas_vindas')))
        response.set_cookie('theme', theme, max_age=1800) 
        flash(f'Tema alterado para {theme}!', 'info')
        return response
    flash('Tema inválido.', 'danger')
    return redirect(request.referrer or url_for('boas_vindas'))


@app.route('/noticias')
def noticias():
    if 'username' not in session:
        flash('Você precisa fazer login para acessar as notícias.', 'danger')
        return redirect(url_for('login'))

    categoria_selecionada = request.args.get('categoria')

    if categoria_selecionada:
        session['last_category'] = categoria_selecionada 
    elif 'last_category' in session:
        categoria_selecionada = session['last_category']
    else:
        categoria_selecionada = 'Todas'

    if categoria_selecionada and categoria_selecionada != 'Todas':
        noticias_filtradas = [n for n in NOTICIAS if n['categoria'] == categoria_selecionada]
    else:
        noticias_filtradas = NOTICIAS

    return render_template('noticias.html', noticias=noticias_filtradas,
                           categorias=['Todas', 'Esportes', 'Entretenimento', 'Lazer'],
                           categoria_ativa=categoria_selecionada)

@app.route('/logout')
def logout():
    session.pop('username', None)     
    session.pop('views', None)        
    session.pop('last_category', None) 
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('registrarUsuario'))

if __name__ == '__main__':
    app.run(debug=True)