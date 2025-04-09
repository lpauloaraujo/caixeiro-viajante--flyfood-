import random

def gerar_populacao_inicial(num_listas, tamanho_lista):
    listas = set()

    while len(listas) < num_listas:
        nova_lista = random.sample(range(1, tamanho_lista + 1), tamanho_lista)
        nova_lista.append(nova_lista[0])  # Adiciona o ciclo no final

        listas.add(tuple(nova_lista))  # Usando set para garantir soluções únicas

    return [list(l) for l in listas]

def encontrarcoordenadas(arquivo):
    with open(arquivo, 'r') as file:
        linhas = [linha.strip().split() for linha in file.readlines()[6:58]]
        lista_coordenadas = {}

        for indice in range(len(linhas)):
            for elemento in range(len(linhas[0])):
                if elemento == 0:
                    lista_coordenadas[str(indice + 1)] = {}
                elif elemento == 1:
                    lista_coordenadas[str(indice + 1)]['X'] = int(float(linhas[indice][elemento]))
                else:
                    lista_coordenadas[str(indice + 1)]['Y'] = int(float(linhas[indice][elemento]))
        return lista_coordenadas

def raiz_quadrada(x, x0, e):
    if abs(x0 ** 2 - x) <= e:
        return x0
    else:
        return raiz_quadrada(x, ((x0 ** 2 + x) / (2 * x0)), e)

def calcular_distancia_solucao(caminho, lista_de_pontos):
    tamanho_do_caminho = 0

    for pos in range(len(caminho) - 1):
        x1, x2 = lista_de_pontos[str(caminho[pos])]['X'], lista_de_pontos[str(caminho[pos + 1])]['X']
        y1, y2 = lista_de_pontos[str(caminho[pos])]['Y'], lista_de_pontos[str(caminho[pos + 1])]['Y']

        x = (x2 - x1) ** 2 + (y2 - y1) ** 2
        distancia_dois_pontos = raiz_quadrada(x, 3.2, 0.0001)
        tamanho_do_caminho += int(distancia_dois_pontos)

    return tamanho_do_caminho

def selecao_torneio(solucoes, listapontos):
    pai1 = random.randint(0, len(solucoes) - 1)
    pai2 = pai1

    while pai2 == pai1:
        pai2 = random.randint(0, len(solucoes) - 1)

    if calcular_distancia_solucao(solucoes[pai1], listapontos) < calcular_distancia_solucao(solucoes[pai2], listapontos):
        paivencedor1 = pai1
    else:
        paivencedor1 = pai2

    pai3 = paivencedor1
    while pai3 == paivencedor1:
        pai3 = random.randint(0, len(solucoes) - 1)

    pai4 = pai3
    while pai4 == pai3:
        pai4 = random.randint(0, len(solucoes) - 1)

    if calcular_distancia_solucao(solucoes[pai3], listapontos) < calcular_distancia_solucao(solucoes[pai4], listapontos):
        paivencedor2 = pai3
    else:
        paivencedor2 = pai4

    return paivencedor1, paivencedor2

def selecao_roleta(solucoes, vagas, listapontos):
    fitnesses = [1 / calcular_distancia_solucao(individuo, listapontos) for individuo in solucoes]
    total_fitness_inverso = sum(fitnesses)
    probabilidades = [fitness / total_fitness_inverso for fitness in fitnesses]
    individuos_selecionados = random.choices(solucoes, weights=probabilidades, k=vagas)

    return individuos_selecionados

def crossover(pai1, pai2):
    ponto_de_corte = random.randint(2, len(pai1) - len(pai1) // 4)
    pai1clone = pai1[:]

    for ponto in range(ponto_de_corte):
        if pai1clone[ponto] != pai2[ponto]:
            pos_do_a_ser_trocado = None

            for indice, point in enumerate(pai1clone):
                if point == pai2[ponto]:
                    pos_do_a_ser_trocado = indice
                    break
            if pos_do_a_ser_trocado is None:
                return random.sample(range(1, len(pai1) + 1), len(pai1) + 1)
            pai1clone[ponto], pai1clone[pos_do_a_ser_trocado] = pai1clone[pos_do_a_ser_trocado], pai1clone[ponto]

    pai1clone[len(pai1clone) - 1] = pai1clone[0]

    return pai1clone

def gerar_filhos(pai1, pai2):
    child1 = crossover(pai1, pai2)
    child2 = crossover(pai2, pai1)
    return child1, child2

def mutacao(solucao, taxa):
    for ponto in range(len(solucao)):
        if random.random() < taxa:
            indice_a_ser_trocado = random.choice([i for i in range(len(solucao)) if i != ponto])

            if ponto == 0 or ponto == len(solucao) - 1:
                ini_fim = solucao[ponto]
                solucao[0] = solucao[indice_a_ser_trocado]
                solucao[len(solucao) - 1] = solucao[indice_a_ser_trocado]
                solucao[indice_a_ser_trocado] = ini_fim
            elif indice_a_ser_trocado == 0 or indice_a_ser_trocado == len(solucao) - 1:
                ini_fim = solucao[indice_a_ser_trocado]
                solucao[0] = solucao[ponto]
                solucao[len(solucao) - 1] = solucao[ponto]
                solucao[ponto] = ini_fim
            else:
                solucao[ponto], solucao[indice_a_ser_trocado] = solucao[indice_a_ser_trocado], solucao[ponto]

    return solucao

def renovar_pop_torneio(pop_atual, tamanho_pop, coordenadas_pontos, taxa_de_mutacao):
    escolhidos = [None] * (tamanho_pop // 2)
    elite = menor_solucao(pop_atual, coordenadas_pontos)[0]

    for _ in range(tamanho_pop // 4):
        possiveis_selecionados = selecao_torneio(pop_atual, coordenadas_pontos)
        while possiveis_selecionados[0] in escolhidos or possiveis_selecionados[1] in escolhidos:
            possiveis_selecionados = selecao_torneio(pop_atual, coordenadas_pontos)
        escolhidos[_] = possiveis_selecionados[0]
        escolhidos[tamanho_pop // 4 + _] = possiveis_selecionados[1]

    escolhidos[0] = elite

    for individuo in range(0, len(escolhidos), 2):
        novos_filhos = gerar_filhos(pop_atual[escolhidos[individuo]], pop_atual[escolhidos[individuo + 1]])
        pop_atual[individuo] = pop_atual[escolhidos[individuo]]
        pop_atual[individuo + 1] = pop_atual[escolhidos[individuo + 1]]
        pop_atual[individuo + tamanho_pop // 2] = mutacao(novos_filhos[0], taxa_de_mutacao)
        pop_atual[individuo + (tamanho_pop // 2) + 1] = mutacao(novos_filhos[1], taxa_de_mutacao)

def renovar_pop_roleta(pop_atual, tamanho_pop, coordenadas_pontos, taxa_de_mutacao):
    escolhidos = selecao_roleta(pop_atual, tamanho_pop // 2, coordenadas_pontos)
    for individuo in range(0, len(escolhidos), 2):
        if random.random() < 0.9:
            novos_filhos = gerar_filhos(escolhidos[individuo], escolhidos[individuo + 1])
            pop_atual[individuo] = escolhidos[individuo]
            pop_atual[individuo + 1] = escolhidos[individuo + 1]
            pop_atual[individuo + tamanho_pop // 2] = mutacao(novos_filhos[0], taxa_de_mutacao)
            pop_atual[individuo + (tamanho_pop // 2) + 1] = mutacao(novos_filhos[1], taxa_de_mutacao)

def menor_solucao(pop, coords):
    tamanhos_populacao_final = [calcular_distancia_solucao(solu, coords) for solu in pop]
    menor_distancia = min(tamanhos_populacao_final)
    respectiva_solucao = tamanhos_populacao_final.index(menor_distancia)

    return respectiva_solucao, menor_distancia

def main():
    tam_pop = 180
    qtd_geracoes = 2000
    taxa_de_mutacao = 0.01
    pop_atual = gerar_populacao_inicial(tam_pop, 52)
    dic_pontos = encontrarcoordenadas('data/berlin52.tsp')

    for _ in range(qtd_geracoes):
        if _ == 1500:
            taxa_de_mutacao = 0.1
        renovar_pop_torneio(pop_atual, tam_pop, dic_pontos, taxa_de_mutacao)

    melhor_indice, menor_distancia = menor_solucao(pop_atual, dic_pontos)
    print(f"Melhor solução encontrada: {pop_atual[melhor_indice]} com distância de {menor_distancia}")

if __name__ == '__main__':
    import timeit
    tempo_de_execucao = timeit.timeit(main, number=1)
    print(f'\nTempo de execução: {tempo_de_execucao:.6f} segundos.')
