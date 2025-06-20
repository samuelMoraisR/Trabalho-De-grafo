import os
from leitor import ler_instancia
from grafo import Grafo
from estatisticas import estatisticas_completas
from rota import Rota

def processar_instancia(caminho_arquivo, pasta_saida='solutions'):

    try:
        dados = ler_instancia(caminho_arquivo)
        if not dados:
            print(f"Erro ao ler {caminho_arquivo}")
            return None
        
        grafo = Grafo(dados)
        print(f"\nProcessando {dados['name']}...")
        
        # etapa1)
        estatisticas_completas(grafo)
        
        # 
        salvar = Rota(grafo)
        rotas, custo_total = salvar.gerar_solucao_inicial()
        
        # Criando pasta de saída caso ñ existir
        os.makedirs(pasta_saida, exist_ok=True)
        
        # salvando a solução.
        nome_arquivo = f"sol-{dados['name']}.dat"
        caminho_saida = os.path.join(pasta_saida, nome_arquivo)
        
        with open(caminho_saida, "w") as f:
            f.write(f"TotalCost {custo_total}\n")
            for i, rota in enumerate(rotas, 1):
                caminho_str = ' '.join(map(str, rota['caminho']))
                f.write(f"Route {i}: {caminho_str} | Load {rota['carga_atual']} | Cost {rota['custo_total']}\n")
        
        print(f"Solução salva em {caminho_saida} (Custo: {custo_total})")
        return custo_total
    
    except Exception as e:
        print(f"Erro ao processar {caminho_arquivo}: {str(e)}")
        return None

def main():
    # Configurações
    pasta_instancias = "data"  
    pasta_saida = "solutions"  
    
    # Processa todos os arquivos .dat da pasta
    print(f"\nIniciando processamento da instancias em '{pasta_instancias}'...")
    
    resultados = []
    for arquivo in os.listdir(pasta_instancias):
        if arquivo.endswith(".dat"):
            caminho_completo = os.path.join(pasta_instancias, arquivo)
            custo = processar_instancia(caminho_completo, pasta_saida)
            if custo is not None:
                resultados.append((arquivo, custo))
    
    # Resumo final
    print("\nResumo dos resultados:")
    for arquivo, custo in resultados:
        print(f"{arquivo:<20} → Custo: {custo}")
    
    print(f"\nTodas as solucoes foram salvas na pasta '{pasta_saida}'")

if __name__ == "__main__":
    main()