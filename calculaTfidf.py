import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def AnalisaVetor(VetorIds: list) -> dict:
    tamanhoVet = len(VetorIds)
    return {VetorIds[i]: (tamanhoVet - i) / tamanhoVet for i in range(tamanhoVet)}


def ListaVideosRelacionados(idVideo):
    listaVideosTranscricao = []
    listaVideosInfo = []
    indice = 0
    cont = 0

    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["BdVideosTranscricao"]
    colecao = db["VideoDados"]
    documentos = colecao.find()

    for doc in documentos:
        for item in doc["Dados"]:
            if (item["Id do video"] == idVideo):
                indice = cont
            listaVideosTranscricao.append(item["Transcricao"])
            aux = item
            del aux["Transcricao"]
            listaVideosInfo.append(aux)
            cont += 1
    cliente.close()

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

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pymongo

def calcularVetorTfidf(colecao):
    listaVideosTranscricao = []
    listaVideosIds = []
    listaVideosInfo = []
    cont = 0

    res = colecao.find()

    for doc in res:
        for item in doc["Dados"]:
            listaVideosTranscricao.append(item["Transcricao"])
            listaVideosIds.append(item["Id do video"])
            aux = item.copy()  # Use .copy() to avoid modifying the original dictionary
            del aux["Transcricao"]
            listaVideosInfo.append(aux)
            cont += 1

    documentos = [' '.join(lista) for lista in listaVideosTranscricao]

    vectorizer = TfidfVectorizer()
    vetores_tfidf = vectorizer.fit_transform(documentos)

    return listaVideosIds, listaVideosInfo, vetores_tfidf

def ListaRecomendacaoSemelhancaVideos(idVideo, colecao, listaVideosIds, listaVideosInfo, vetores_tfidf):
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
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["BdVideosTranscricao"]
    colecao = db["VideoDados"]

    listaVideosIds, listaVideosInfo, vetores_tfidf = calcularVetorTfidf(colecao)
    listaDicionarios = []

    for item in listaVideos:
        print(item)
        vetIds, vetInfo = ListaRecomendacaoSemelhancaVideos(item, colecao, listaVideosIds, listaVideosInfo, vetores_tfidf)
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

    cliente.close()
    somaTotalDicionarios = dict(sorted(somaTotalDicionarios.items(), key=lambda item: item[1], reverse=True))
    listaChaves = list(somaTotalDicionarios.keys())
    [listaChaves.remove(item) for item in listaVideos if item in listaChaves]
    resposta = [vetInfo[item] for item in listaChaves]
    return resposta

def ListaVideosHistoricos(listaVideos: list):
    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["BdVideosTranscricao"]
    colecao = db["VideoDados"]

    listaVideosInfo = []

    for item in listaVideos:
        res = colecao.find_one({"Dados.Id do video": item})
        if res:
            video_info = next((v for v in res["Dados"] if v["Id do video"] == item), None)
            if video_info:
                del video_info["Transcricao"]
                listaVideosInfo.append(video_info)

    listaVideosInfo = listaVideosInfo[::-1]

    cliente.close()

    return listaVideosInfo

def ListaVideosBusca(texto):
    listaVideosTranscricao = []
    listaVideosInfo = []

    cliente = pymongo.MongoClient("mongodb://localhost:27017/")
    db = cliente["BdVideosTranscricao"]
    colecao = db["VideoDados"]
    documentos = colecao.find()

    for doc in documentos:
        for item in doc["Dados"]:
            listaVideosTranscricao.append(item["Transcricao"])
            aux = item
            del aux["Transcricao"]
            listaVideosInfo.append(aux)
    cliente.close()

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
