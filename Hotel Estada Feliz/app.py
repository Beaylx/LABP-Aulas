from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'chave-secreta-hotel-123'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(80), nullable=False)
    perfil = db.Column(db.String(20), nullable=False)

class Quarto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True, nullable=False)
    tipo = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(16), default='Limpo')
    preco = db.Column(db.Float, nullable=False)

class Hospede(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    cpf = db.Column(db.String(20), unique=True)
    telefone = db.Column(db.String(30))

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospede = db.Column(db.String(80), nullable=False)
    quarto = db.Column(db.String(10), nullable=False)
    checkin = db.Column(db.String(16))
    checkout = db.Column(db.String(16))
    status = db.Column(db.String(20), default='Confirmada')


PERFIS = ["Administrador", "Recepcionista", "Camareira"]


@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = Usuario.query.filter_by(email=email, senha=senha).first()
        if user:
            session['user'] = {'id': user.id, 'perfil': user.perfil, 'nome': user.nome, 'email': user.email}
            flash('Login realizado com sucesso!', 'success')
            if user.perfil == 'Administrador':
                return redirect(url_for('admin'))
            elif user.perfil == 'Recepcionista':
                return redirect(url_for('recepcao'))
            elif user.perfil == 'Camareira':
                return redirect(url_for('camareira'))
        else:
            flash('Email ou senha inválidos!', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado!', 'info')
    return redirect(url_for('login'))

# ADMIN
@app.route('/admin')
def admin():
    if 'user' not in session or session['user']['perfil'] != 'Administrador':
        return redirect(url_for('login'))
    usuarios = Usuario.query.all()
    quartos = Quarto.query.all()
    return render_template('admin.html', usuario=session['user'],
                          usuarios=usuarios, quartos=quartos, perfis=PERFIS)

@app.route('/add-usuario', methods=['POST'])
def add_usuario():
    if 'user' not in session or session['user']['perfil'] != 'Administrador':
        return redirect(url_for('login'))
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    perfil = request.form.get('perfil')
    novo = Usuario(nome=nome, email=email, senha=senha, perfil=perfil)
    db.session.add(novo)
    db.session.commit()
    flash('Usuário adicionado!', 'success')
    return redirect(url_for('admin'))

@app.route('/del-usuario/<int:id>', methods=['POST'])
def del_usuario(id):
    if 'user' not in session or session['user']['perfil'] != 'Administrador':
        return redirect(url_for('login'))
    Usuario.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Usuário excluído!', 'success')
    return redirect(url_for('admin'))

@app.route('/add-quarto', methods=['POST'])
def add_quarto():
    if 'user' not in session or session['user']['perfil'] != 'Administrador':
        return redirect(url_for('login'))
    numero = request.form.get('numero')
    tipo = request.form.get('tipo')
    preco = float(request.form.get('preco'))
    novo = Quarto(numero=numero, tipo=tipo, preco=preco)
    db.session.add(novo)
    db.session.commit()
    flash('Quarto adicionado!', 'success')
    return redirect(url_for('admin'))

@app.route('/del-quarto/<int:id>', methods=['POST'])
def del_quarto(id):
    if 'user' not in session or session['user']['perfil'] != 'Administrador':
        return redirect(url_for('login'))
    Quarto.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Quarto excluído!', 'success')
    return redirect(url_for('admin'))

# RECEPCAO
@app.route('/recepcao')
def recepcao():
    if 'user' not in session or session['user']['perfil'] != 'Recepcionista':
        return redirect(url_for('login'))
    reservas = Reserva.query.all()
    hospedes = Hospede.query.all()
    quartos = Quarto.query.all()
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
    nova = Reserva(hospede=hospede, quarto=quarto, checkin=checkin, checkout=checkout)
    db.session.add(nova)
    db.session.commit()
    flash('Reserva criada!', 'success')
    return redirect(url_for('recepcao'))

@app.route('/del-reserva/<int:id>', methods=['POST'])
def del_reserva(id):
    if 'user' not in session or session['user']['perfil'] != 'Recepcionista':
        return redirect(url_for('login'))
    Reserva.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Reserva excluída!', 'success')
    return redirect(url_for('recepcao'))

@app.route('/add-hospede', methods=['POST'])
def add_hospede():
    if 'user' not in session or session['user']['perfil'] != 'Recepcionista':
        return redirect(url_for('login'))
    nome = request.form.get('nome')
    cpf = request.form.get('cpf')
    telefone = request.form.get('telefone')
    novo = Hospede(nome=nome, cpf=cpf, telefone=telefone)
    db.session.add(novo)
    db.session.commit()
    flash('Hóspede cadastrado!', 'success')
    return redirect(url_for('recepcao'))

@app.route('/del-hospede/<int:id>', methods=['POST'])
def del_hospede(id):
    if 'user' not in session or session['user']['perfil'] != 'Recepcionista':
        return redirect(url_for('login'))
    Hospede.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Hóspede excluído!', 'success')
    return redirect(url_for('recepcao'))

# CAMAREIRA
@app.route('/camareira')
def camareira():
    if 'user' not in session or session['user']['perfil'] != 'Camareira':
        return redirect(url_for('login'))
    quartos = Quarto.query.all()
    return render_template('camareira.html', usuario=session['user'], quartos=quartos)

@app.route('/update-quarto/<int:id>', methods=['POST'])
def update_quarto(id):
    if 'user' not in session or session['user']['perfil'] != 'Camareira':
        return redirect(url_for('login'))
    novo_status = request.form.get('status')
    quarto = Quarto.query.get(id)
    quarto.status = novo_status
    db.session.commit()
    flash('Status atualizado!', 'success')
    return redirect(url_for('camareira'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        if not Usuario.query.first():
            db.session.add(Usuario(nome="Carlos Admin",email="admin@hotel.com",senha="admin123",perfil="Administrador"))
            db.session.add(Usuario(nome="Ana Recepcionista",email="recepcao@hotel.com",senha="recepcao123",perfil="Recepcionista"))
            db.session.add(Usuario(nome="Maria Camareira",email="camareira@hotel.com",senha="camareira123",perfil="Camareira"))
            db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
