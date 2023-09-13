# Suponha que você tenha três listas ordenadas com os mesmos valores
lista1 = ["A", "B", "C", "D"]
lista2 = ["D", "C", "B", "A"]
lista3 = ["B", "D", "A", "C"]

# Defina os pesos para cada lista
peso_lista1 = 0.3
peso_lista2 = 0.4
peso_lista3 = 0.3

# Combine as três listas em uma única lista
listas_combinadas = [lista1, lista2, lista3]

# Crie um dicionário para armazenar a contagem de ocorrências de cada valor
contagem_ocorrencias = {}

# Percorra as listas e atualize a contagem de ocorrências com os pesos
for i, lista in enumerate(listas_combinadas):
    peso = [peso_lista1, peso_lista2, peso_lista3][i]
    for valor in lista:
        if valor in contagem_ocorrencias:
            contagem_ocorrencias[valor] += peso
        else:
            contagem_ocorrencias[valor] = peso

# Agora, calcule a média ponderada
lista_final = []
for valor, peso_total in contagem_ocorrencias.items():
    lista_final.extend([valor] * peso_total)

# Ordene a lista final se necessário
lista_final.sort()

print(lista_final)
