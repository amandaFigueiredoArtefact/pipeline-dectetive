from . import ai_client
from . import ocr_processor
from . import visualizer

# --- PROMPT ESPECIALIZADO PARA JSON ---
JSON_PROMPT = """
Você é um especialista em análise de pipelines de dados. Analise o seguinte conteúdo de pipeline, que está em formato JSON.
Sua tarefa é extrair a linhagem de dados e retorná-la em um formato JSON estruturado.

O JSON de saída deve ter duas chaves principais: "nodes" e "edges".
- "nodes": Uma lista de todos os componentes (fontes, destinos, transformações). Cada nó deve ter "id", "label" e "type" ('source', 'target', 'transformation').
- "edges": Uma lista de todas as conexões entre os nós, com "source" e "target".

IMPORTANTE: Sua resposta deve conter APENAS o código JSON válido derivado da análise do conteúdo JSON fornecido. Não inclua texto extra. Sua resposta deve começar com `{` e terminar com `}`.
"""

# --- PROMPT ESPECIALIZADO E MELHORADO PARA SQL ---
SQL_PROMPT = """
Você é um especialista em análise de código SQL. Analise o seguinte script SQL para extrair a linhagem de dados a nível de tabela.
Sua tarefa é identificar as tabelas de origem, a tabela de destino e as principais operações de transformação, e retornar essa informação em um formato JSON estruturado.

O JSON de saída deve ter duas chaves principais: "nodes" e "edges".

- "nodes":
  - Identifique todas as tabelas de origem (de onde os dados são lidos, ex: FROM e JOINs) e classifique-as com `type: 'source'`.
  - Identifique a tabela de destino (para onde os dados são escritos, ex: CREATE TABLE, INSERT INTO) e classifique-a com `type: 'target'`.
  - Crie um único nó de transformação (`type: 'transformation'`) que resuma a lógica do script. Para o "label" deste nó, crie uma descrição concisa que inclua as principais operações, como "JOIN, WHERE, GROUP BY".

- "edges":
  - Crie conexões de todas as tabelas de origem para o nó de transformação.
  - Crie uma conexão do nó de transformação para a tabela de destino.

Exemplo de label para o nó de transformação: "Transformação (JOIN, WHERE, GROUP BY)"

IMPORTANTE: Sua resposta deve conter APENAS o código JSON válido derivado da análise do script SQL fornecido. Não inclua texto extra. Sua resposta deve começar com `{` e terminar com `}`.
"""

# --- PROMPT ESPECIALIZADO PARA YAML ---
YAML_PROMPT = """
Você é um especialista em análise de pipelines de dados. Analise o seguinte conteúdo de pipeline, que está em formato YAML.
Sua tarefa é extrair a linhagem de dados e retorná-la em um formato JSON estruturado.

O JSON de saída deve ter duas chaves principais: "nodes" e "edges".
- "nodes": Uma lista de todos os componentes (fontes, destinos, transformações). Cada nó deve ter "id", "label" e "type" ('source', 'target', 'transformation').
- "edges": Uma lista de conexões entre os nós, com "source" e "target".

IMPORTANTE: Sua resposta deve conter APENAS o código JSON válido derivado da análise do conteúdo YAML fornecido. Não inclua texto extra. Sua resposta deve começar com `{` e terminar com `}`.
"""

# --- PROMPT ESPECIALIZADO E MELHORADO PARA IMAGEM/OCR ---
IMAGE_PROMPT = """
Você é um especialista em análise de pipelines de dados. O texto a seguir foi extraído de uma IMAGEM usando OCR e pode estar confuso.
Sua tarefa é interpretar este texto, identificar os componentes da pipeline e suas conexões, e retornar essa informação em um formato JSON estruturado.

O JSON de saída deve ter duas chaves principais: "nodes" e "edges".
- "nodes": Uma lista de todos os componentes. Cada nó deve ter "id", "label" e "type".
  - Use o tipo 'source' para nós que são pontos de partida, especialmente se contiverem a palavra "Fonte".
  - Use o tipo 'target' para nós que são pontos de chegada finais, especialmente se contiverem a palavra "Destino".
  - Use o tipo 'transformation' para todos os outros nós que representam uma operação ou passo intermediário.
- "edges": Uma lista de conexões entre os nós que você inferir do fluxo.

IMPORTANTE: Sua resposta deve conter APENAS o código JSON válido derivado da sua interpretação do texto. Não inclua explicações sobre o processo. Sua resposta deve começar com `{` e terminar com `}`.
"""

def generate_from_content(content_bytes: bytes, file_type: str, ai_provider: str) -> str:
    """
    Orquestra a geração do diagrama de linhagem a partir do conteúdo de um ficheiro.
    """
    structured_data = None
    text_content = ""
    prompt_template = "" # Usaremos uma única variável para o template

    if file_type in ['png', 'jpg', 'jpeg']:
        text_content = ocr_processor.get_text_from_image(content_bytes)
        prompt_template = IMAGE_PROMPT
    else:
        text_content = content_bytes.decode("utf-8")
        if file_type == 'json': prompt_template = JSON_PROMPT
        elif file_type == 'sql': prompt_template = SQL_PROMPT
        elif file_type in ['yaml', 'yml']: prompt_template = YAML_PROMPT
    
    if not text_content or not prompt_template:
        print(f"Conteúdo para análise vazio ou tipo de arquivo não suportado: {file_type}")
        return None

    # Monta o prompt final para ambos os provedores de IA
    full_prompt = f"{prompt_template}\n\nConteúdo para analisar:\n{text_content}"
    system_prompt = prompt_template
    user_prompt = f"Analise o seguinte conteúdo:\n\n{text_content}"

    # Chama a IA
    if ai_provider.lower() == 'gemini':
        print("Enviando prompt especializado para a IA (Gemini)...")
        structured_data = ai_client.get_gemini_response(full_prompt)
    elif ai_provider.lower() == 'chatgpt':
        print("Enviando prompt especializado para a IA (ChatGPT)...")
        structured_data = ai_client.get_chatgpt_response(system_prompt, user_prompt)
    else:
        raise ValueError("Provedor de IA desconhecido.")

    if not structured_data:
        print("Falha ao obter dados da IA.")
        return None
    
    return visualizer.generate_lineage_image(structured_data)
