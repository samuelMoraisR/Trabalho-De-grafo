from leitor import ler_instancia
from grafo import Grafo
from estatisticas import estatisticas_completas

def main():
    # Carrega a instância (altere para o arquivo desejado)
    caminho_arquivo = "data/BHW1.dat"
    dados = ler_instancia(caminho_arquivo)
    
    if not dados:
        print("Falha ao carregar os dados.")
        return
    
    # Cria a estrutura do grafo
    grafo = Grafo(dados)
    
    # Calcula e exibe estatísticas
    estatisticas_completas(grafo)
    
    # Exemplo de uso adicional
    matriz_dist = grafo.matriz_distancias()
    print(f"Distância entre 1 e 2: {matriz_dist[1][2]}")
    print(f"Componentes conexos: {grafo.componentes_conexos()}")

if __name__ == "__main__":
    main()