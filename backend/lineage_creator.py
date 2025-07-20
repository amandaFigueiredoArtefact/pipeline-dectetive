# backend/lineage_creator.py

from . import ai_client # Aponta para o novo nome do arquivo
from . import ocr_processor
from . import visualizer

# Instrução base que funciona para ambos os modelos
BASE_PROMPT_INSTRUCTION = """
Você é um especialista em análise de pipelines de dados. Analise o conteúdo fornecido. Sua tarefa é extrair a linhagem de dados e retorná-la em um formato JSON estruturado.
O JSON de saída deve ter duas chaves principais: "nodes" e "edges".
- "nodes": Uma lista de todos os componentes. Cada nó deve ter "id" (um nome único sem espaços), "label" (o nome para exibição) e "type" ('source', 'target', ou 'transformation').
- "edges": Uma lista de conexões entre os nós. Cada aresta deve ter "source" (o id do nó de origem) e "target" (o id do nó de destino).

IMPORTANTE: Sua resposta deve conter APENAS o código JSON válido, sem nenhum texto, explicação ou formatação markdown como ```json no início ou ``` no final.
"""

# Templates específicos para cada tipo de conteúdo
JSON_PROMPT_ADDON = f"{BASE_PROMPT_INSTRUCTION}\nO conteúdo a ser analisado está em formato JSON."
SQL_PROMPT_ADDON = f"{BASE_PROMPT_INSTRUCTION}\nO conteúdo a ser analisado é um script SQL."
YAML_PROMPT_ADDON = f"{BASE_PROMPT_INSTRUCTION}\nO conteúdo a ser analisado está em formato YAML."
IMAGE_PROMPT_ADDON = f"{BASE_PROMPT_INSTRUCTION}\nO conteúdo a ser analisado foi extraído de uma imagem via OCR e pode conter erros. Interprete-o da melhor forma possível."

# Função atualizada para aceitar o provedor de IA como um argumento
def generate_from_content(content_bytes: bytes, file_type: str, ai_provider: str) -> str:
    structured_data = None
    text_content = ""
    system_prompt = ""

    # Processamento de Input (OCR para imagens, decodificação para texto)
    if file_type in ['png', 'jpg', 'jpeg']:
        print("Arquivo de imagem detectado. Processando com OCR...")
        text_content = ocr_processor.get_text_from_image(content_bytes)
        system_prompt = IMAGE_PROMPT_ADDON
    else:
        text_content = content_bytes.decode("utf-8")
        if file_type == 'json': system_prompt = JSON_PROMPT_ADDON
        elif file_type == 'sql': system_prompt = SQL_PROMPT_ADDON
        elif file_type in ['yaml', 'yml']: system_prompt = YAML_PROMPT_ADDON
    
    if not text_content:
        print("Conteúdo para análise está vazio.")
        return None

    # Lógica para escolher qual cliente de IA chamar
    if ai_provider.lower() == 'gemini':
        full_prompt = f"{system_prompt}\n\nConteúdo para analisar:\n{text_content}"
        print("Enviando prompt para a IA (Gemini)...")
        structured_data = ai_client.get_gemini_response(full_prompt)

    elif ai_provider.lower() == 'chatgpt':
        user_prompt = f"Analise o seguinte conteúdo:\n\n{text_content}"
        print("Enviando prompt para a IA (ChatGPT)...")
        structured_data = ai_client.get_chatgpt_response(system_prompt, user_prompt)
        
    else:
        raise ValueError("Provedor de IA desconhecido.")

    if not structured_data:
        print("Falha ao obter dados da IA.")
        return None
    
    return visualizer.generate_lineage_image(structured_data)