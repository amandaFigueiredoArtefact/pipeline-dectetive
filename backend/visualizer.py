import graphviz

def generate_lineage_image(data: dict, output_filename: str = "lineage_diagram") -> str:
    """
    Gera uma imagem de diagrama de linhagem de dados a partir de dados estruturados.
    
    Args:
        data (dict): Dicionário com 'nodes' e 'edges'.
        output_filename (str): Nome do arquivo de saída sem a extensão.

    Returns:
        str: O caminho para a imagem gerada (ex: 'lineage_diagram.png').
    """
    if not data or 'nodes' not in data or 'edges' not in data:
        print("Erro: Dados de entrada para o visualizador estão inválidos ou vazios.")
        return None

    # Cria um novo gráfico direcionado (Digraph)
    dot = graphviz.Digraph(comment='Data Lineage', format='png')
    dot.attr(rankdir='LR', splines='ortho') # Da esquerda para a direita
    dot.attr('node', shape='box', style='rounded,filled', color='skyblue', fontname='Arial')
    dot.attr('edge', color='gray40', arrowsize='0.7', fontname='Arial', fontsize='10')

    # Adiciona os nós (tabelas, transformações) ao gráfico
    for node in data['nodes']:
        # Personaliza a cor baseada no tipo de nó
        node_color = 'lightgreen' if node['type'] == 'source' else \
                     'lightcoral' if node['type'] == 'target' else \
                     'khaki'
        dot.node(node['id'], label=node['label'], color=node_color)

    # Adiciona as arestas (conexões) ao gráfico
    for edge in data['edges']:
        dot.edge(edge['source'], edge['target'], label=edge.get('label', ''))
    
    try:
        # Renderiza (salva) o gráfico em um arquivo de imagem
        output_path = dot.render(output_filename, cleanup=True)
        print(f"Diagrama salvo em: {output_path}")
        return output_path
    except Exception as e:
        print(f"Erro ao renderizar o gráfico com Graphviz: {e}")
        return None