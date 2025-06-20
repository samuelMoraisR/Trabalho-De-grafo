import re
import sys
from collections import defaultdict

def ler_instancia(caminho_arquivo):
    
    """aqui lê um arquivo de instância e estamos retornando um dicionário estruturado com os dados"""

    try:
        with open(caminho_arquivo, 'r') as f:
            linhas = f.readlines()
    except Exception as e:
        print(f"Erro ao ler arquivo: {str(e)}", file=sys.stderr)
        return None

    dados = {
        'name': "",
        'optimal_value': -1,
        'num_vehicles': -1,
        'capacity': -1,
        'depot': -1,
        'num_nodes': 0,
        'num_edges': 0,
        'num_arcs': 0,
        'required_nodes': {},
        'required_edges': [],
        'required_arcs': [],
        'non_required_edges': [],
        'non_required_arcs': []
    }

    secao = None

    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith(("the data is", "Instance")):
            continue

        # Processa metadados
        if ':' in linha and not linha.startswith(("ReN", "ReE", "ReA", "EDGE", "ARC")):
            chave, valor = [parte.strip() for parte in linha.split(':', 1)]
            
            if chave == "Name":
                dados['name'] = valor
            elif chave == "Optimal value":
                dados['optimal_value'] = int(valor) if valor != "-1" else -1
            elif chave == "#Vehicles":
                dados['num_vehicles'] = int(valor)
            elif chave == "Capacity":
                dados['capacity'] = int(valor)
            elif chave == "Depot Node":
                dados['depot'] = int(valor)
            elif chave == "#Nodes":
                dados['num_nodes'] = int(valor)
            elif chave == "#Edges":
                dados['num_edges'] = int(valor)
            elif chave == "#Arcs":
                dados['num_arcs'] = int(valor)
            continue

        # Identifica seções
        if linha.startswith("ReN"):
            secao = "ReN"
            continue
        elif linha.startswith("ReE"):
            secao = "ReE"
            continue
        elif linha.startswith("ReA"):
            secao = "ReA"
            continue
        elif linha.startswith("EDGE"):
            secao = "NRE"
            continue
        elif linha.startswith("ARC"):
            secao = "NRA"
            continue

        # Processa conteúdo das seções
        partes = re.split(r'\s+', linha)
        
        try:
            if secao == "ReN" and len(partes) >= 3:
                node_id = int(partes[0].replace('N', ''))
                dados['required_nodes'][node_id] = {
                    'demand': int(partes[1]),
                    'service_cost': int(partes[2])
                }
                
            elif secao == "ReE" and len(partes) >= 6:
                dados['required_edges'].append({
                    'id': partes[0],
                    'from': int(partes[1]),
                    'to': int(partes[2]),
                    't_cost': int(partes[3]),
                    'demand': int(partes[4]),
                    's_cost': int(partes[5])
                })
                
            elif secao == "ReA" and len(partes) >= 6:
                dados['required_arcs'].append({
                    'id': partes[0],
                    'from': int(partes[1]),
                    'to': int(partes[2]),
                    't_cost': int(partes[3]),
                    'demand': int(partes[4]),
                    's_cost': int(partes[5])
                })
                
            elif secao == "NRE" and len(partes) >= 4:
                dados['non_required_edges'].append({
                    'id': partes[0],
                    'from': int(partes[1]),
                    'to': int(partes[2]),
                    't_cost': int(partes[3])
                })
                
            elif secao == "NRA" and len(partes) >= 4:
                dados['non_required_arcs'].append({
                    'id': partes[0],
                    'from': int(partes[1]),
                    'to': int(partes[2]),
                    't_cost': int(partes[3])
                })
                
        except (ValueError, IndexError) as e:
            print(f"AVISO: Ignorando linha mal formatada - {linha}", file=sys.stderr)
            continue

    return dados