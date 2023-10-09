import json

from flask import Flask,jsonify,request
from flask_cors import CORS
from calculaTfidf import ListaVideosRelacionados,ListaVideosBusca,ListaVideosRecomendados,ListaVideosRecomendadosRestrita,ListaVideosHistoricos,AdicionaPlaylistSugestoes

app = Flask(__name__)

CORS(app)

@app.route('/processa_relacionados', methods=['GET'])
def processa_relacionados():
    video_id = request.args.get('query')
    resposta = ListaVideosRelacionados(video_id)
    return jsonify(resposta)

@app.route('/processa_trilha', methods=['GET'])
def processa_trilha():
    lista = request.args.get('historico')
    lista2 = lista.replace("[", "")
    lista3 = lista2.replace("]", "")
    lista4 = lista3.replace("\"", "")
    lista4 = lista4.replace(" ","")
    listaFinal = lista4.split(",")
    for i in listaFinal:
        print(i)
    print(listaFinal)
    resposta = ListaVideosRecomendados(listaFinal)
    return jsonify(resposta)

@app.route('/processa_trilha_restrita', methods=['GET'])
def processa_trilha_restrita():
    lista = request.args.get('historico')
    lista2 = lista.replace("[", "")
    lista3 = lista2.replace("]", "")
    lista4 = lista3.replace("\"", "")
    lista4 = lista4.replace(" ","")
    listaFinal = lista4.split(",")
    listaplaylist=request.args.get('playlists')
    lista2 = listaplaylist.replace("[", "")
    lista3 = lista2.replace("]", "")
    lista4 = lista3.replace("\"", "")
    lista4 = lista4.replace(" ", "")
    listaFinal2 = lista4.split(",")
    print(listaFinal)
    print(listaFinal2)
    resposta = ListaVideosRecomendadosRestrita(listaFinal,listaFinal2)
    return jsonify(resposta)

@app.route('/processa_historico', methods=['GET'])
def processa_historico():
    lista = request.args.get('historico')
    lista2 = lista.replace("[", "")
    lista3 = lista2.replace("]", "")
    lista4 = lista3.replace("\"", "")
    lista4 = lista4.replace(" ","")
    listaFinal = lista4.split(",")
    for i in listaFinal:
        print(i)
    print(listaFinal)
    resposta = ListaVideosHistoricos(listaFinal)
    return jsonify(resposta)

@app.route('/processa_busca', methods=['GET'])
def processa_busca():
    frase_busca = request.args.get('query')
    resposta = ListaVideosBusca(frase_busca)
    return jsonify(resposta)

@app.route(rule='/adiciona_sugestao',methods=['GET'])
def adiciona_sugestao():
    idPlaylist = request.args.get('id')
    nomePlaylist = request.args.get('nome')
    resposta = AdicionaPlaylistSugestoes(idPlaylist,nomePlaylist)
    return jsonify(resposta)

@app.route("/")
def home():
    return "Hello, World!"    

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')