from flask import Flask, render_template, jsonify
app = Flask(__name__)

dados_biografias = {
    "santos_domunt": {
        "nome": "Santos Dumont",
        "texto": "Alberto Santos Dumont foi um aeronauta, esportista e inventor brasileiro..."
    }
}

@app.route("/")

def index():
    personagens = dados_biografias.keys()

    return render_template("index.html", personagens=personagens, nomes=dados_biografias)

@app.route("/biografia/<id_personagem>")

def get_biografia(id_personagem):

    """
    Busca dados do personagem no noso dicionário
    Usa .get() para retornar um valor padraõ caso o id não seja encontrado
    """


    
    biografia_data = dados_biografias.get(id_personagem, {
        "nome": "Desconhecido",
        "texto": "Personagem não encontrado"
    })

    return jsonify(biografia_data)

if __name__ == "__main__":
    app.run(debug=True) 
