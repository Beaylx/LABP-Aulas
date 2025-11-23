from flask import Flask, render_template, abort

app = Flask(__name__)

#Rota principal

@app.route('/')

def index():
    returnnrender_template('index.html')

#Para demonstrar o erro 401, vamos criar uma rota que exige login (simulaod)

@app.route('/area-restrita')

def area_restrita():

    #Em uma aplicação real, aqui você verificaria se o usuário está logado

    #Como não temos um sistema de login vamos forçar o erro 401 com abort().

    print("Tentativa de acesso à área restrita sem autenticação.")

abort(401)

#Para demonstrar um erro 403, uma ota de admin (simulado)

@app.route('/painel-admin')

def painel_admin():

    # Aqui vc verifica se o user logado é um adm

    # Vamos simular q o user não é adm e forçar o erro 403

    print("Tentativa de acesso ao paibel de admin sem permissão!!")

    abort(403)

#-- Manipuladore de erro (Error Handlers) --

@app.errorhandler(404)

def pagina_nao_encontrada(error):

    return render_template('404.html'), 404

@app.errorhandler(401)

def nao_autorizado(error):

    return render_template('401.html'), 401

@app.errorhandler(403)

def acesso_proibido(error):

    return render_template('403.tml'), 403

if __name__ == "__main__":
    app.run(debug=True)
