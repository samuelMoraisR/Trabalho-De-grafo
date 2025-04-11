from collections import defaultdict

class Grafo:
    def __init__(self, dados):
        self.dados = dados
        self.num_nodes = dados['num_nodes']
        self.vertices = set(range(1, dados['num_nodes'] + 1))
        
        # Conexões
        self.arestas = dados['required_edges'] + dados.get('non_required_edges', [])
        self.arcos = dados['required_arcs'] + dados.get('non_required_arcs', [])
        
        # criamos estruturas auxiliares
        self.adjacencia = defaultdict(list)
        self.graus = defaultdict(int)
        self._construir_grafo()
    
    def _construir_grafo(self):
        """tamo construindo a estrutura de adjacência do grafo here"""
        for aresta in self.arestas:
            u, v = aresta['from'], aresta['to']
            self.adjacencia[u].append((v, False))  # caso for False indica aresta não direcionada
            self.adjacencia[v].append((u, False))
            self.graus[u] += 1
            self.graus[v] += 1
            
        for arco in self.arcos:
            u, v = arco['from'], arco['to']
            self.adjacencia[u].append((v, True))  # True indica arco (direcionado)
            self.graus[u] += 1
    
    def calcular_graus(self):
        """estou retornando  o grau de cada nó"""
        return self.graus
    
    def matriz_distancias(self):
        """ fizemos uma matriz de distâncias mínimas usando Floyd-Warshall"""
        n = self.num_nodes
        dist = [[float('inf')] * (n + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            dist[i][i] = 0
            
        # Processa arestas (bidirecionais)
        for aresta in self.arestas:
            u, v, custo = aresta['from'], aresta['to'], aresta['t_cost']
            dist[u][v] = min(dist[u][v], custo)
            dist[v][u] = min(dist[v][u], custo)
            
        # Processa arcos (direcionais)
        for arco in self.arcos:
            u, v, custo = arco['from'], arco['to'], arco['t_cost']
            dist[u][v] = min(dist[u][v], custo)
        
        # Algoritmo Floyd-Warshall
        for k in range(1, n + 1):
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    if dist[i][j] > dist[i][k] + dist[k][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
        
        return dist
    
    def componentes_conexos(self):
        """i dentifica componentes conexos (considerando arestas como bidirecionais)"""
        visitados = set()
        componentes = []
        
        for no in range(1, self.num_nodes + 1):
            if no not in visitados:
                componente = []
                pilha = [no]
                
                while pilha:
                    atual = pilha.pop()
                    if atual not in visitados:
                        visitados.add(atual)
                        componente.append(atual)
                        for vizinho, _ in self.adjacencia.get(atual, []):
                            pilha.append(vizinho)
                
                componentes.append(componente)
        
        return componentes
    
    def calcular_intermediacao(self):
        """Calcula a intermediação (betweenness centrality) aproximada"""
        intermediacao = defaultdict(int)
        
        for s in range(1, self.num_nodes + 1):
            for t in range(1, self.num_nodes + 1):
                if s != t:
                    caminho = self.encontrar_caminho_minimo(s, t)
                    if caminho:
                        for no in caminho[1:-1]:  # Ignora os extremos
                            intermediacao[no] += 1
        
        return intermediacao
    
    def encontrar_caminho_minimo(self, origem, destino):
        """Busca em largura para encontrar caminho mínimo"""
        from collections import deque
        
        fila = deque()
        fila.append((origem, [origem]))
        visitados = set()
        
        while fila:
            atual, caminho = fila.popleft()
            
            if atual == destino:
                return caminho
                
            if atual not in visitados:
                visitados.add(atual)
                for vizinho, _ in self.adjacencia.get(atual, []):
                    fila.append((vizinho, caminho + [vizinho]))
        
        return None
    
    def calcular_diametro_caminho_medio(self):
        """Calcula diâmetro e caminho médio baseado na matriz de distâncias"""
        distancias = self.matriz_distancias()
        valores = []
        
        for i in range(1, self.num_nodes + 1):
            for j in range(i + 1, self.num_nodes + 1):
                if distancias[i][j] != float('inf'):
                    valores.append(distancias[i][j])
        
        caminho_medio = sum(valores) / len(valores) if valores else 0
        diametro = max(valores) if valores else 0
        
        return diametro, caminho_medio