# backend/lineage_creator.py

from . import gemini_client
from . import visualizer

# Prompts pré-definidos que serão enviados para a IA
JSON_PROMPT_TEMPLATE = """
Você é um especialista em análise de pipelines de dados. Analise o seguinte conteúdo de pipeline, que está em formato JSON.
Sua tarefa é extrair a linhagem de dados e retorná-la em um formato JSON estruturado.

O JSON de saída deve ter duas chaves principais: "nodes" e "edges".
- "nodes": Uma lista de todos os componentes (fontes, destinos, transformações). Cada nó deve ter "id" (um nome único sem espaços), "label" (o nome para exibição) e "type" ('source', 'target', ou 'transformation').
- "edges": Uma lista de todas as conexões entre os nós. Cada aresta deve ter "source" (o id do nó de origem) e "target" (o id do nó de destino).

Conteúdo da pipeline para analisar:
{content}
"""

SQL_PROMPT_TEMPLATE = """
Você é um especialista em análise de código SQL. Analise o seguinte script SQL para extrair a linhagem de dados.
Sua tarefa é identificar as tabelas de origem, a tabela de destino e as principais transformações, e retornar essa informação em um formato JSON estruturado.

O JSON de saída deve ter duas chaves principais: "nodes" e "edges".
- "nodes": Identifique as tabelas de origem (type: 'source'), a tabela de destino (type: 'target') e a operação principal (ex: 'SELECT com JOIN', type: 'transformation'). Cada nó deve ter "id", "label" e "type".
- "edges": Crie conexões das fontes para a transformação, e da transformação para o destino. Cada aresta deve ter "source" e "target".

Script SQL para analisar:
{content}
"""

def generate_from_content(content: str, file_type: str) -> str:
    """
    Orquestra a geração do diagrama de linhagem a partir do conteúdo de um arquivo.

    Args:
        content (str): O conteúdo do arquivo (JSON ou SQL).
        file_type (str): O tipo de arquivo ('json' ou 'sql').

    Returns:
        str: O caminho para a imagem do diagrama gerado, ou None se falhar.
    """
    prompt = ""
    if file_type == 'json':
        prompt = JSON_PROMPT_TEMPLATE.format(content=content)
    elif file_type == 'sql':
        prompt = SQL_PROMPT_TEMPLATE.format(content=content)
    else:
        print(f"Tipo de arquivo não suportado: {file_type}")
        return None

    print("Enviando prompt para a IA...")
    # Chama o cliente Gemini para obter os dados estruturados
    structured_data = gemini_client.get_gemini_response(prompt)

    if not structured_data:
        print("Falha ao obter dados da IA.")
        return None
    
    print("Dados recebidos da IA. Gerando diagrama...")
    # Chama o visualizador para criar a imagem do diagrama
    image_path = visualizer.generate_lineage_image(structured_data)

    return image_path