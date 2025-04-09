from collections import deque
import time
import tracemalloc

movimentos = {
    'Cima': (-1, 0),
    'Baixo': (1, 0),
    'Esquerda': (0, -1),
    'Direita': (0, 1)
}

class NoPuzzle:
    def __init__(self, estado, pai=None, movimento=None, nivel=0):
        self.estado = estado
        self.pai = pai
        self.movimento = movimento
        self.nivel = nivel

    def __hash__(self):
        return hash(str(self.estado))

    def __eq__(self, outro):
        return self.estado == outro.estado

def encontrar_zero(estado):
    for i in range(3):
        for j in range(3):
            if estado[i][j] == 0:
                return i, j

def gerar_filhos(no):
    filhos = []
    linha_zero, coluna_zero = encontrar_zero(no.estado)

    for direcao, (dl, dc) in movimentos.items():
        nova_linha = linha_zero + dl
        nova_coluna = coluna_zero + dc

        if 0 <= nova_linha < 3 and 0 <= nova_coluna < 3:
            novo_estado = [list(linha) for linha in no.estado]
            novo_estado[linha_zero][coluna_zero], novo_estado[nova_linha][nova_coluna] = \
                novo_estado[nova_linha][nova_coluna], novo_estado[linha_zero][coluna_zero]
            novo_estado_tupla = tuple(tuple(linha) for linha in novo_estado)
            filhos.append(NoPuzzle(novo_estado_tupla, no, direcao, no.nivel + 1))

    return filhos

def estado_objetivo(estado):
    return estado == ((1, 2, 3), (4, 5, 6), (7, 8, 0))

def reconstruir_caminho(no):
    caminho = []
    while no.pai:
        caminho.append(no.movimento)
        no = no.pai
    caminho.reverse()
    return caminho

def bfs(estado_inicial):
    raiz = NoPuzzle(estado_inicial)
    fila = deque([raiz])
    visitados = set()
    visitados.add(raiz)

    max_fronteira = 1
    max_profundidade = 0

    while fila:
        atual = fila.popleft()
        if estado_objetivo(atual.estado):
            return {
                'caminho': reconstruir_caminho(atual),
                'custo': atual.nivel,
                'nos_expandidos': len(visitados),
                'fronteira': len(fila),
                'max_fronteira': max_fronteira,
                'profundidade': atual.nivel,
                'max_profundidade': max(max_profundidade, atual.nivel)
            }

        for filho in gerar_filhos(atual):
            if filho not in visitados:
                fila.append(filho)
                visitados.add(filho)
                max_fronteira = max(max_fronteira, len(fila))
                max_profundidade = max(max_profundidade, filho.nivel)

def dfs(estado_inicial, limite=50):
    raiz = NoPuzzle(estado_inicial)
    pilha = [raiz]
    visitados = set()

    max_fronteira = 1
    max_profundidade = 0

    while pilha:
        atual = pilha.pop()
        if estado_objetivo(atual.estado):
            return {
                'caminho': reconstruir_caminho(atual),
                'custo': atual.nivel,
                'nos_expandidos': len(visitados),
                'fronteira': len(pilha),
                'max_fronteira': max_fronteira,
                'profundidade': atual.nivel,
                'max_profundidade': max(max_profundidade, atual.nivel)
            }

        if atual not in visitados and atual.nivel <= limite:
            visitados.add(atual)
            filhos = gerar_filhos(atual)
            for filho in reversed(filhos):  # Reverso para simular ordem correta na pilha
                if filho not in visitados:
                    pilha.append(filho)
                    max_fronteira = max(max_fronteira, len(pilha))
                    max_profundidade = max(max_profundidade, filho.nivel)

def iddfs(estado_inicial, limite_maximo=30):
    for limite in range(limite_maximo + 1):
        resultado = dfs(estado_inicial, limite)
        if resultado:
            return resultado

def ler_puzzle_usuario():
    print("Digite os 9 números do puzzle separados por espaço (use 0 para o espaço vazio):")
    entrada = list(map(int, input().split()))
    return tuple(tuple(entrada[i:i+3]) for i in range(0, 9, 3))

def escolher_algoritmo():
    print("\nEscolha o algoritmo de busca:")
    print("1 - Busca em Largura (BFS)")
    print("2 - Busca em Profundidade (DFS)")
    print("3 - Busca em Profundidade Iterativa (IDDFS)")
    return input("Digite o número da opção: ")

if __name__ == "__main__":
    puzzle_inicial = ler_puzzle_usuario()
    escolha = escolher_algoritmo()

    inicio = time.time()
    tracemalloc.start()

    if escolha == '1':
        resultado = bfs(puzzle_inicial)
        nome_algoritmo = "BFS"
    elif escolha == '2':
        resultado = dfs(puzzle_inicial)
        nome_algoritmo = "DFS"
    elif escolha == '3':
        resultado = iddfs(puzzle_inicial)
        nome_algoritmo = "IDDFS"
    else:
        print("Opção inválida.")
        exit()

    tempo_total = time.time() - inicio
    memoria_usada, _ = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if resultado:
        print(f"\nalgoritmo: {nome_algoritmo}")
        print(f"path_to_goal: {resultado['caminho']}")
        print(f"cost_of_path: {resultado['custo']}")
        print(f"nodes_expanded: {resultado['nos_expandidos']}")
        print(f"fringe_size: {resultado['fronteira']}")
        print(f"max_fringe_size: {resultado['max_fronteira']}")
        print(f"search_depth: {resultado['profundidade']}")
        print(f"max_search_depth: {resultado['max_profundidade']}")
        print(f"running_time: {tempo_total:.8f}")
        print(f"max_ram_usage: {memoria_usada / 1024:.8f}")
    else:
        print(f"\nO algoritmo {nome_algoritmo} não encontrou solução dentro dos limites definidos.")