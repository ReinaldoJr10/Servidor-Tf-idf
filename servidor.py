from flask import Flask,jsonify,request
from calculaTfidf import ListaRecomendacaoHistorico,ListaRecomendacaoBusca

app = Flask(__name__)

@app.route('/processa_recomendacao', methods=['GET'])
def processa_recomendacao():
    video_id = request.args.get('query')
    resposta = ListaRecomendacaoHistorico(video_id)
    return jsonify(resposta)

@app.route('/processa_busca', methods=['GET'])
def processa_busca():
    frase_busca = request.args.get('query')
    resposta = ListaRecomendacaoBusca(frase_busca)
    return jsonify(resposta)

@app.route("/")
def home():
    return "Hello, World!"    

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='10.0.0.24')