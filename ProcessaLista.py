
def AnalisaVetor(VetorIds: list) -> dict:
    tamanhoVet = len(VetorIds)
    return {VetorIds[i]: (tamanhoVet - i) / tamanhoVet for i in range(tamanhoVet)}

