from flask import Flask, render_template, request, flash, redirect, utl_for
app = Flask(__name__)

#Secret key necessaria para usar flash massages

app.config[ 'SECRET_KEY' ] = 'uma-chave-secreta-muiti-segura'

@app.route(' /formulario', methods= ['GET', 'POST'])
def formulario ():
    
    if request.method == 'POST':
        
        #Em uma aplicação real, aqui ocorreria a validação no back-end

        nome = request.form.get('nome')
        email = request.form.get('email')

        print(f'Dados Recebidos do formulári: Nome={nome}, Email={email}')

        #Simula uma menssagem de sucesso

        flash(f'Obrigada por se cadastrar, {nome}!', 'Sucess')

        return redirect(url_for('formulario'))
    
    return render_template('formulario.html')