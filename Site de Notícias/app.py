from flask import Flask, render_template, request, flash, redirect, url_for, session, make_response

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

usuarios_cadastrados = []
USUARIO_FIXO = {'username': 'teste', 'password': '123'}

NOTICIAS = [
    {'titulo': 'Brasil vence o Mundial de Vôlei!', 'categoria': 'Esportes', 'conteudo': 'A seleção brasileira de vôlei masculino conquistou o título mundial após uma campanha impecável.'},
    {'titulo': 'Novo filme de comédia arrasa nas bilheterias', 'categoria': 'Entretenimento', 'conteudo': 'O filme "Risadas Garantidas" está fazendo um sucesso estrondoso, com críticas positivas e recordes de público.'},
    {'titulo': 'Dicas para um final de semana relaxante', 'categoria': 'Lazer', 'conteudo': 'Descubra atividades para aproveitar seu tempo livre, recarregar as energias e fugir da rotina estressante.'},
    {'titulo': 'Recorde de medalhas para o Brasil nas Olimpíadas', 'categoria': 'Esportes', 'conteudo': 'Os atletas brasileiros brilharam nas pistas e piscinas, superando as expectativas e conquistando um número histórico de medalhas.'},
    {'titulo': 'Show beneficente arrecada fundos para hospitais', 'categoria': 'Entretenimento', 'conteudo': 'Grandes nomes da música se reuniram em um evento inesquecível, arrecadando milhões para a causa da saúde pública.'},
    {'titulo': 'Explorando trilhas ecológicas na Amazônia', 'categoria': 'Lazer', 'conteudo': 'Uma aventura única pela maior floresta tropical do mundo, com guias especializados e paisagens de tirar o fôlego.'},
    {'titulo': 'Campeonato Brasileiro acirrado até a última rodada', 'categoria': 'Esportes', 'conteudo': 'A disputa pelo título está mais emocionante do que nunca, com vários times na briga até os minutos finais da competição.'},
    {'titulo': 'Série de TV de sucesso renovada para nova temporada', 'categoria': 'Entretenimento', 'conteudo': 'Os fãs da série já podem comemorar a continuação da história que conquistou milhões de espectadores em todo o mundo.'},
    {'titulo': 'Culinária gourmet para o fim de semana', 'categoria': 'Lazer', 'conteudo': 'Receitas fáceis e saborosas para impressionar seus convidados e desfrutar de momentos deliciosos em casa.'},
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