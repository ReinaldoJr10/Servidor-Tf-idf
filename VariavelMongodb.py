import os

def recuperar_variavel_ambiente(nome_variavel):
    valor_variavel = os.environ.get(nome_variavel)
    if valor_variavel is not None:
        return valor_variavel
    else:
        return f"A variável de ambiente '{nome_variavel}' não foi encontrada."
