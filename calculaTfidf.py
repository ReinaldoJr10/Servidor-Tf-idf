import pandas as pd
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def ListaRecomendacao(id):
    with open('playlist.json', 'r') as arquivo:
        dados = json.load(arquivo)

    listaListasPalavras=[]
    listaTitulos = []
    listaVideoIds = []
    indice=0
    cont=0

    for instancia in dados:
        for chave, valores in instancia.items():
            for valor in valores:
                if(id==valor["Id do video"]):
                    indice=cont                    
                listaTitulos.append(valor["Titulo"])
                listaVideoIds.append(valor["Id do video"])
                listaListasPalavras.append(valor["Transcricao"])
                cont+=1

    documentos = [' '.join(lista) for lista in listaListasPalavras]

    # Crie um objeto TfidfVectorizer
    vectorizer = TfidfVectorizer()

    # Ajuste o vetorizador aos documentos e transforme-os em vetores TF-IDF
    vetores_tfidf = vectorizer.fit_transform(documentos)

    vetor_item_interagido = vetores_tfidf[indice]
    # Calcula a similaridade de cosseno entre 'vetor_item_interagido' e todos os outros vetores TF-IDF
    similaridades = cosine_similarity(vetores_tfidf, vetor_item_interagido)

    # Obtém os índices dos itens mais semelhantes, classificados em ordem decrescente de similaridade
    indices_itens_similares = similaridades.argsort(axis=0)[:-1, 0][::-1]

    itens_recomendados = [listaTitulos[i] for i in indices_itens_similares]
    itens_ids = [listaVideoIds[i] for i in indices_itens_similares]

    print(listaTitulos[indice])
    print("--------------------------------------")
    for i in range(10):
        print(itens_recomendados[i])
        print(itens_ids[i])
    return itens_ids
        