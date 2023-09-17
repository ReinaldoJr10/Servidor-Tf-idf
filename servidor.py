
from flask import Flask,jsonify,request
from calculaTfidf import ListaRecomendacaoHistoricoMongo,ListaRecomendacaoBuscaMongo

app = Flask(__name__)

@app.route('/processa_recomendacao_mongo', methods=['GET'])
def processa_recomendacao_mongo():
    video_id = request.args.get('query')
    lista = request.args.get('playlist')
    lista2 = lista.replace("[", "")
    lista3 = lista2.replace("]", "")
    lista4 = lista3.replace("\"", "")
    listaFinal = lista4.split(",")
    resposta = ListaRecomendacaoHistoricoMongo(video_id,listaFinal)
    return jsonify(resposta)

@app.route('/processa_busca_mongo', methods=['GET'])
def processa_busca_mongo():
    frase_busca = request.args.get('query')
    resposta = ListaRecomendacaoBuscaMongo(frase_busca)
    return jsonify(resposta)

@app.route("/")
def home():
    return "Hello, World!"    

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='10.0.0.24')