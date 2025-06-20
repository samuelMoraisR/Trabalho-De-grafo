class Rota:
    def __init__(self, grafo):
        self.grafo = grafo
        self.dados = grafo.dados
        self.distancias = grafo.matriz_distancias()
        self.deposito = grafo.dados['depot']
        self.capacidade = grafo.dados['capacity']
        self.servicos_requeridos = grafo.dados['required_edges'] + grafo.dados['required_arcs']
    
    def criar_rota_vazia(self):
        """Cria uma rota vazia pronta para ser preenchida"""
        return {
            'servicos': [],
            'carga_atual': 0,
            'custo_total': 0,
            'caminho': [self.deposito]
        }
    
    def adicionar_servico(self, rota, servico, custo_viagem, vertice_chegada):
        """Adiciona um serviço a uma rota existente"""
        rota['custo_total'] += custo_viagem + servico['s_cost']
        rota['carga_atual'] += servico['demand']
        rota['servicos'].append(servico)
        rota['caminho'].append(vertice_chegada)
        return rota
    
    def finalizar_rota(self, rota, custo_retorno):
        """Finaliza uma rota adicionando o retorno ao deposito"""
        rota['custo_total'] += custo_retorno
        rota['caminho'].append(self.deposito)
        return rota
    
    def gerar_solucao_inicial(self):
        """utilizamos o Algoritmo Path Scanning para gerar solução inicial"""
        servicos_restantes = {(s['from'], s['to'], s['id']) for s in self.servicos_requeridos}
        rotas = []
        
        while servicos_restantes:
            rota = self.criar_rota_vazia()
            posicao_atual = self.deposito
            
            while True:
                # Filtra serviços viáveis
                servicos_faceis = [
                    s for s in self.servicos_requeridos 
                    if (s['from'], s['to'], s['id']) in servicos_restantes
                    and rota['carga_atual'] + s['demand'] <= self.capacidade
                ]
                
                if not servicos_faceis:
                    break
                
                # Seleciona o mais próximo (regra 1 do Path Scanning)
                servico = min(
                    servicos_faceis,
                    key=lambda s: min(
                        self.distancias[posicao_atual][s['from']],
                        self.distancias[posicao_atual][s['to']]
                    )
                )
                
                # Decide orientação
                if self.distancias[posicao_atual][servico['from']] <= self.distancias[posicao_atual][servico['to']]:
                    custo_viagem = self.distancias[posicao_atual][servico['from']]
                    chegada = servico['to']
                else:
                    custo_viagem = self.distancias[posicao_atual][servico['to']]
                    chegada = servico['from']
                
                # Atualiza rota
                rota = self.adicionar_servico(rota, servico, custo_viagem, chegada)
                servicos_restantes.remove((servico['from'], servico['to'], servico['id']))
                posicao_atual = chegada
            
            # Finaliza a rota
            rota = self.finalizar_rota(rota, self.distancias[posicao_atual][self.deposito])
            rotas.append(rota)
        
        custo_total = sum(r['custo_total'] for r in rotas)
        return rotas, custo_total