import json

import pymongo
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def ListaRecomendacaoHistoricoMongo(idVideo,listaPlaylist):
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
            if(item["Id do video"]==idVideo):
                indice=cont
            listaVideosTranscricao.append(item["Transcricao"])
            aux=item
            del aux["Transcricao"]
            listaVideosInfo.append(aux)
            cont+=1
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
    print("Busca realizada!!!")
    # for i in range(10):
    #    print(itens_recomendados[i])
    #    print(itens_ids[i])
    return itens_info

def ListaRecomendacaoBuscaMongo(texto):

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
