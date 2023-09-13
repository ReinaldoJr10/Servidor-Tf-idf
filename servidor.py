from flask import Flask,jsonify,request
from calculaTfidf import ListaRecomendacao
from montaDadosPlaylist import processa_dados

app = Flask(__name__)

@app.route('/processa_recomendacao', methods=['GET'])
def processa_recomendacao():
    video_id = request.args.get('query')
    resposta = ListaRecomendacao(video_id)
    # Faça o processamento necessário no Python
    result = {"message": "Dados processados com sucesso!"}
    return jsonify(resposta)

@app.route("/")
def home():
    return "Hello, World!"    

if __name__ == "__main__":
    app.run(debug=True)