from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json,os
from montaDadosPlaylist import ProcessaPlaylist

def QtdPlaylistBd() -> int:
    my_dir = os.path.dirname(__file__)
    json_caminho = os.path.join(my_dir, 'dados.json')
    with open(json_caminho, 'r') as arquivo_json:
        dados = json.load(arquivo_json)
    return len(dados)

def verifica_inclusao_playlist(idPlaylist:str) -> bool:
    my_dir = os.path.dirname(__file__)
    json_caminho = os.path.join(my_dir, 'dados.json')
    with open(json_caminho, 'r') as arquivo_json:
        dados = json.load(arquivo_json)
    for i in range(len(dados)):
        if(dados[i]["idPlaylist"]==idPlaylist):
            return True
    return False

def AdicionaPlaylistBd(idPlaylist:str,nomePlaylist:str):
    resultado=verifica_inclusao_playlist(idPlaylist)
    if resultado:
        return "ja esta na playlist"
    else:
        json_novo=ProcessaPlaylist(idPlaylist,nomePlaylist)
        my_dir = os.path.dirname(__file__)
        json_caminho = os.path.join(my_dir, 'dados.json')
        with open(json_caminho, 'r+') as arquivo:
            dados = json.load(arquivo)
            dados.append(json_novo)
            arquivo.seek(0)
            json.dump(dados, arquivo, indent=4)
        return "valor adicionado"+str(QtdPlaylistBd())

def AnalisaVetor(VetorIds: list) -> dict:
    tamanhoVet = len(VetorIds)
    return {VetorIds[i]: (tamanhoVet - i) / tamanhoVet for i in range(tamanhoVet)}


def ListaVideosRelacionados(idVideo):
    my_dir = os.path.dirname(__file__)
    json_caminho = os.path.join(my_dir, 'dados.json')
    listaVideosTranscricao = []
    listaVideosInfo = []
    indice = 0
    cont = 0

    with open(json_caminho, 'r') as arquivo_json:
        dados = json.load(arquivo_json)

    for i in range(len(dados)):
        for y in range(len(dados[i]["Dados"])):
            if (dados[i]["Dados"][y]["Id do video"] == idVideo):
                indice = cont
            listaVideosTranscricao.append(dados[i]["Dados"][y]["Transcricao"])
            aux = dados[i]["Dados"][y]
            del aux["Transcricao"]
            listaVideosInfo.append(aux)
            cont+=1

    documentos = [' '.join(lista) for lista in listaVideosTranscricao]

    # Crie um objeto TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # Ajuste o vetorizador aos documentos e transforme-os em vetores TF-IDF
    vetores_tfidf = vectorizer.fit_transform(documentos)

    vetor_item_interagido = vetores_tfidf[indice]

    # Calcula a similaridade de cosseno entre 'vetor_item_interagido' e todos os outros vetores TF-IDF
    similaridades = cosine_similarity(vetores_tfidf, vetor_item_interagido)

    # Obtém os índices dos itens mais semelhantes, classificados em ordem decrescente de similaridade
    indices_itens_similares = similaridades.argsort(axis=0)[:-1, 0][::-1]

    itens_info = [listaVideosInfo[i] for i in indices_itens_similares]

    # print(texto)
    print("--------------------------------------")
    print("Recomendacao realizada!!!")
    return itens_info

def calcularVetorTfidf():
    my_dir = os.path.dirname(__file__)
    json_caminho = os.path.join(my_dir, 'dados.json')
    listaVideosTranscricao = []
    listaVideosIds = []
    listaVideosInfo = []
    cont = 0

    with open(json_caminho, 'r') as arquivo_json:
        dados = json.load(arquivo_json)

    for i in range(len(dados)):
        for y in range(len(dados[i]["Dados"])):
            listaVideosTranscricao.append(dados[i]["Dados"][y]["Transcricao"])
            listaVideosIds.append(dados[i]["Dados"][y]["Id do video"])
            aux=dados[i]["Dados"][y]
            del aux["Transcricao"]
            listaVideosInfo.append(aux)
            cont += 1

    documentos = [' '.join(lista) for lista in listaVideosTranscricao]

    vectorizer = TfidfVectorizer()
    vetores_tfidf = vectorizer.fit_transform(documentos)

    return listaVideosIds, listaVideosInfo, vetores_tfidf

def ListaRecomendacaoSemelhancaVideos(idVideo, listaVideosIds, listaVideosInfo, vetores_tfidf):
    indice = listaVideosIds.index(idVideo)
    vetor_item_interagido = vetores_tfidf[indice]

    similaridades = cosine_similarity(vetores_tfidf, vetor_item_interagido)

    indices_itens_similares = similaridades.argsort(axis=0)[:-1, 0][::-1]

    itens_ids = [listaVideosIds[i] for i in indices_itens_similares]
    itens_info = [listaVideosInfo[i] for i in indices_itens_similares]

    itens_info_dict = {item["Id do video"]: item for item in itens_info}

    print("--------------------------------------")
    print("Semelhança encontrada!!!")
    return itens_ids, itens_info_dict

def ListaVideosRecomendados(listaVideos: list):

    listaVideosIds, listaVideosInfo, vetores_tfidf = calcularVetorTfidf()
    listaDicionarios = []


    for item in listaVideos:
        print(item)
        vetIds, vetInfo = ListaRecomendacaoSemelhancaVideos(item, listaVideosIds, listaVideosInfo, vetores_tfidf)
        auxs = AnalisaVetor(vetIds)
        print(auxs)
        if item in auxs:
            del auxs[item]
            del vetInfo[item]
        listaDicionarios.append(auxs)

    somaTotalDicionarios = {}
    for itemDicionario in listaDicionarios:
        for item in itemDicionario:
            if item in somaTotalDicionarios:
                somaTotalDicionarios[item] += itemDicionario[item]
            else:
                somaTotalDicionarios[item] = itemDicionario[item]

    somaTotalDicionarios = dict(sorted(somaTotalDicionarios.items(), key=lambda item: item[1], reverse=True))
    listaChaves = list(somaTotalDicionarios.keys())
    [listaChaves.remove(item) for item in listaVideos if item in listaChaves]
    resposta = [vetInfo[item] for item in listaChaves]
    return resposta

def ler_dados_do_arquivo_json():
    my_dir = os.path.dirname(__file__)
    json_caminho = os.path.join(my_dir, 'dados.json')
    with open(json_caminho, 'r', encoding='utf-8') as arquivo:
        dados_json = json.load(arquivo)
    return dados_json

def ListaVideosHistoricos(listaVideos: list):
    # Lê os dados do arquivo JSON
    dados = ler_dados_do_arquivo_json()

    listaVideosInfo = []

    for item in listaVideos:
        for i in range(len(dados)):
            for y in range(len(dados[i]["Dados"])):
                if dados[i]["Dados"][y]["Id do video"] == item:
                    aux = dados[i]["Dados"][y]
                    del aux["Transcricao"]
                    listaVideosInfo.append(aux)

    listaVideosInfo = listaVideosInfo[::-1]

    return listaVideosInfo

def ListaVideosBusca(texto):
    my_dir = os.path.dirname(__file__)
    json_caminho = os.path.join(my_dir, 'dados.json')
    listaVideosTranscricao = []
    listaVideosInfo = []

    with open(json_caminho, 'r') as arquivo_json:
        dados = json.load(arquivo_json)

    for i in range(len(dados)):
        for y in range(len(dados[i]["Dados"])):
            listaVideosTranscricao.append(dados[i]["Dados"][y]["Transcricao"])
            aux = dados[i]["Dados"][y]
            del aux["Transcricao"]
            listaVideosInfo.append(aux)


    documentos = [' '.join(lista) for lista in listaVideosTranscricao]
    documentos.append(texto)

    vectorizer = TfidfVectorizer()

    vetores_tfidf = vectorizer.fit_transform(documentos)

    vetor_item_interagido = vetores_tfidf[len(listaVideosTranscricao)]

    similaridades = cosine_similarity(vetores_tfidf, vetor_item_interagido)

    indices_itens_similares = similaridades.argsort(axis=0)[:-1, 0][::-1]

    itens_info = [listaVideosInfo[i] for i in indices_itens_similares]

    print("--------------------------------------")
    print("Busca realizada!!!")
    return itens_info
