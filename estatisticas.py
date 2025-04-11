def estatisticas_completas(grafo):
    
    """Calcula e exibe todas as estatísticas requeridas na Etapa 1"""
    # Métricas básicas


    total_arestas = len(grafo.arestas)
    total_arcos = len(grafo.arcos)
    print(f"Total de arestas: {total_arestas}")
    print(f"Total de arcos: {total_arcos}")

    print(f"Número total de vértices: {grafo.num_nodes}")
    print(f"Arestas requeridas: {len(grafo.dados['required_edges'])}")
    print(f"Arcos requeridos: {len(grafo.dados['required_arcs'])}")
    print(f"Vértices requeridos: {len(grafo.dados['required_nodes'])}")
    
    # Graus
    graus = grafo.calcular_graus()
    print(f"\nDistribuição de graus:")
    print(f"Grau máximo: {max(graus.values())}")
    print(f"Grau mínimo: {min(graus.values())}")
    print(f"Grau do depósito ({grafo.dados['depot']}): {grafo.graus[grafo.dados['depot']]}")
    
    # Densidade
    total_conexoes = len(grafo.arestas) + len(grafo.arcos)
    possiveis_conexoes = grafo.num_nodes * (grafo.num_nodes - 1)
    densidade = total_conexoes / possiveis_conexoes
    print(f"\nDensidade do grafo: {densidade:.4f}")
    
    # Componentes conexos
    componentes = grafo.componentes_conexos()
    print(f"\nComponentes conexos: {len(componentes)}")
    print(f"Tamanho do maior componente: {max(len(c) for c in componentes)}")
    print(f"Tamanho do menor componente: {min(len(c) for c in componentes)}")
    
    # Distancias
    diametro, caminho_medio = grafo.calcular_diametro_caminho_medio()
    print(f"\nDiametro do grafo: {diametro}")
    print(f"Caminho médio: {caminho_medio:.2f}")
    
    # Intermediação
    intermediacao = grafo.calcular_intermediacao()
    no_mais_central = max(intermediacao.items(), key=lambda x: x[1]) if intermediacao else (None, 0)
    print(f"\nNó com maior intermediação: {no_mais_central[0]} (valor: {no_mais_central[1]})")
    


    # Distancias especificas
    distancias = grafo.matriz_distancias()
    deposito = grafo.dados['depot']
    print(f"\nDistancias a partir do deposito {deposito}:")
    for no in sorted(grafo.dados['required_nodes'].keys()):
        distancia = distancias[deposito][no]
        print(f"  → Nó {no}: {distancia if distancia != float('inf') else 'inacessivel'}")