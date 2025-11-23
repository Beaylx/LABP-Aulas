from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response

app = Flask(__name__)
app.secret_key = 'chave-secreta-hotel-123'

perfis = ['Administrador', 'Recepcionista', 'Camareira']

usuarios = [
    {'id': 1, 'email': 'admin@hotel.com', 'senha': 'admin123', 'perfil': 'Administrador', 'nome': 'Carlos Admin'},
    {'id': 2, 'email': 'recepcao@hotel.com', 'senha': 'recepcao123', 'perfil': 'Recepcionista', 'nome': 'Ana Recepcionista'},
    {'id': 3, 'email': 'camareira@hotel.com', 'senha': 'camareira123', 'perfil': 'Camareira', 'nome': 'Maria Camareira'}
]

quartos = [
    {'id': 1, 'numero': '101', 'tipo': 'Simples', 'status': 'Limpo', 'preco': 150.00},
    {'id': 2, 'numero': '102', 'tipo': 'Duplo', 'status': 'Sujo', 'preco': 250.00},
    {'id': 3, 'numero': '201', 'tipo': 'Luxo', 'status': 'Limpo', 'preco': 450.00}
]

reservas = [
    {'id': 1, 'hospede': 'João Silva', 'quarto': '101', 'checkin': '2025-11-20', 'checkout': '2025-11-25', 'status': 'Confirmada'}
]

hospedes = [
    {'id': 1, 'nome': 'João Silva', 'cpf': '123.456.789-00', 'telefone': '(11) 98765-4321'}
]

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = next((u for u in usuarios if u['email'] == email and u['senha'] == senha), None)
        if user:
            session['user'] = {'id': user['id'], 'perfil': user['perfil'], 'nome': user['nome'], 'email': user['email']}
            flash('Login realizado com sucesso!', 'success')
            if user['perfil'] == 'Administrador':
                return redirect(url_for('admin'))
            elif user['perfil'] == 'Recepcionista':
                return redirect(url_for('recepcao'))
            elif user['perfil'] == 'Camareira':
                return redirect(url_for('camareira'))
        else:
            flash('Email ou senha inválidos!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado!', 'info')
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'user' not in session or session['user']['perfil'] != 'Administrador':
        return redirect(url_for('login'))
    cor_fundo = request.cookies.get('cor_fundo', '#f5f5f5')
    return render_template('admin.html', usuario=session['user'],
                          usuarios=usuarios, quartos=quartos, perfis=perfis, cor_fundo=cor_fundo)

@app.route('/add-usuario', methods=['POST'])
def add_usuario():
    if 'user' not in session or session['user']['perfil'] != 'Administrador':
        return redirect(url_for('login'))
    email = request.form.get('email')
    senha = request.form.get('senha')
    perfil = request.form.get('perfil')
    nome = request.form.get('nome')
    new_id = max(u['id'] for u in usuarios) + 1 if usuarios else 1
    usuarios.append({'id': new_id, 'email': email, 'senha': senha, 'perfil': perfil, 'nome': nome})
    flash('Usuário adicionado!', 'success')
    return redirect(url_for('admin'))

@app.route('/del-usuario/<int:id>', methods=['POST'])
def del_usuario(id):
    if 'user' not in session or session['user']['perfil'] != 'Administrador':
        return redirect(url_for('login'))
    global usuarios
    usuarios = [u for u in usuarios if u['id'] != id]
    flash('Usuário excluído!', 'success')
    return redirect(url_for('admin'))

@app.route('/add-quarto', methods=['POST'])
def add_quarto():
    if 'user' not in session or session['user']['perfil'] != 'Administrador':
        return redirect(url_for('login'))
    numero = request.form.get('numero')
    tipo = request.form.get('tipo')
    preco = float(request.form.get('preco'))
    new_id = max(q['id'] for q in quartos) + 1 if quartos else 1
    quartos.append({'id': new_id, 'numero': numero, 'tipo': tipo, 'status': 'Limpo', 'preco': preco})
    flash('Quarto adicionado!', 'success')
    return redirect(url_for('admin'))

@app.route('/del-quarto/<int:id>', methods=['POST'])
def del_quarto(id):
    if 'user' not in session or session['user']['perfil'] != 'Administrador':
        return redirect(url_for('login'))
    global quartos
    quartos = [q for q in quartos if q['id'] != id]
    flash('Quarto excluído!', 'success')
    return redirect(url_for('admin'))

@app.route('/recepcao')
def recepcao():
    if 'user' not in session or session['user']['perfil'] != 'Recepcionista':
        return redirect(url_for('login'))
    return render_template('recepcao.html', usuario=session['user'],
                          reservas=reservas, hospedes=hospedes, quartos=quartos)

@app.route('/add-reserva', methods=['POST'])
def add_reserva():
    if 'user' not in session or session['user']['perfil'] != 'Recepcionista':
        return redirect(url_for('login'))
    hospede = request.form.get('hospede')
    quarto = request.form.get('quarto')
    checkin = request.form.get('checkin')
    checkout = request.form.get('checkout')
    new_id = max(r['id'] for r in reservas) + 1 if reservas else 1
    reservas.append({'id': new_id, 'hospede': hospede, 'quarto': quarto, 'checkin': checkin,
                     'checkout': checkout, 'status': 'Confirmada'})
    flash('Reserva criada!', 'success')
    return redirect(url_for('recepcao'))

@app.route('/del-reserva/<int:id>', methods=['POST'])
def del_reserva(id):
    if 'user' not in session or session['user']['perfil'] != 'Recepcionista':
        return redirect(url_for('login'))
    global reservas
    reservas = [r for r in reservas if r['id'] != id]
    flash('Reserva excluída!', 'success')
    return redirect(url_for('recepcao'))

@app.route('/add-hospede', methods=['POST'])
def add_hospede():
    if 'user' not in session or session['user']['perfil'] != 'Recepcionista':
        return redirect(url_for('login'))
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    telefone = request.form.get('telefone')
    new_id = max(h['id'] for h in hospedes) + 1 if hospedes else 1
    hospedes.append({'id': new_id, 'nome': nome, 'cpf': cpf, 'telefone': telefone})
    flash('Hóspede cadastrado!', 'success')
    return redirect(url_for('recepcao'))

@app.route('/del-hospede/<int:id>', methods=['POST'])
def del_hospede(id):
    if 'user' not in session or session['user']['perfil'] != 'Recepcionista':
        return redirect(url_for('login'))
    global hospedes
    hospedes = [h for h in hospedes if h['id'] != id]
    flash('Hóspede excluído!', 'success')
    return redirect(url_for('recepcao'))

@app.route('/camareira', methods=['GET', 'POST'])
def camareira():
    if 'user' not in session or session['user']['perfil'] != 'Camareira':
        return redirect(url_for('login'))
    return render_template('camareira.html', usuario=session['user'], quartos=quartos)

@app.route('/update-quarto/<int:id>', methods=['POST'])
def update_quarto(id):
    if 'user' not in session or session['user']['perfil'] != 'Camareira':
        return redirect(url_for('login'))
    novo_status = request.form.get('status')
    for quarto in quartos:
        if quarto['id'] == id:
            quarto['status'] = novo_status
            flash('Status atualizado!', 'success')
    return redirect(url_for('camareira'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
