def interpretarmatriz(arquivo):
    arquivomatriz = open(arquivo, 'r')
    matrizoriginal = arquivomatriz.readlines()

    matrizinterpretada = [[None] * int(matrizoriginal[0].split()[1]) for _ in range(int(matrizoriginal[0].split()[0]))]

    for indice in range(len(matrizinterpretada)):
        linhaatual = matrizoriginal[indice + 1].split()

        for coluna in range(len(matrizinterpretada[indice])):
            matrizinterpretada[indice][coluna] = linhaatual[coluna]

    arquivomatriz.close()

    return matrizinterpretada


matriz = interpretarmatriz('matriz.txt')


def pontosdeentrega(mat):
    possibilidadess = []
    for linha in mat:

        for elemento in linha:

            if elemento != '0' and elemento != 'R':
                possibilidadess.append(elemento)
    return ''.join(possibilidadess)


listapontos = pontosdeentrega(matriz)


def possibilidades(sequence):
    if len(sequence) <= 1:
        return [sequence]
    else:
        result = []
        for perm in possibilidades(sequence[1:]):
            for i in range(len(sequence)):
                result.append(perm[:i] + sequence[0:1] + perm[i:])
        return result


def encontrarcoordenadas(matri, segmento):
    lista_coordenadas = []
    for ponto in segmento:
        for i in range(len(matri)):
            for j in range(len(matri[0])):
                if matri[i][j] == ponto:
                    lista_coordenadas.append((i, j))
    return lista_coordenadas


def somar_caminho(mt, caminho):
    coords = encontrarcoordenadas(mt, caminho)
    tamanho_do_caminho = 0
    for indice, vertice in enumerate(coords):
        if indice < len(caminho) - 1:
            distancia_horizontal = abs(abs(vertice[0]) - abs(coords[indice + 1][0]))
            distancia_vertical = abs(abs(vertice[1]) - abs(coords[indice + 1][1]))
            tamanho_do_caminho += distancia_horizontal
            tamanho_do_caminho += distancia_vertical
    return tamanho_do_caminho


def decidir_caminho_de_menor_custo(m, permutacoes):
    caminhos_ordenados = {}
    for indicee, permutacao in enumerate(permutacoes):
        tamanho = somar_caminho(m, permutacao)
        caminhos_ordenados[f'{permutacao}'] = tamanho
    menor_caminho = (None, float('inf'))
    for key, valor in caminhos_ordenados.items():
        if valor <= menor_caminho[1]:
            menor_caminho = (key, valor)
    return print(menor_caminho)


permutacoespossiveis = ['R' + permut + 'R' for permut in possibilidades(listapontos)]
decidir_caminho_de_menor_custo(matriz, permutacoespossiveis)
