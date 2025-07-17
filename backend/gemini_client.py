import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis de ambiente (sua chave de API) do arquivo .env
load_dotenv()

def get_gemini_response(prompt: str) -> dict:
    """
    Envia um prompt para a API do Gemini e retorna a resposta como um dicionário Python.
    """
    try:
        # Configura o SDK do Gemini com a chave de API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Chave de API do Gemini não encontrada. Verifique o arquivo .env")
        
        genai.configure(api_key=api_key)

        # Define o modelo que será usado
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # Envia o prompt para o modelo
        response = model.generate_content(prompt)

        # Limpa a resposta para extrair apenas o conteúdo JSON
        # A IA às vezes retorna o JSON dentro de um bloco de código markdown ```json ... ```
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '').strip()
        
        # Converte a string JSON limpa em um dicionário Python
        return json.loads(cleaned_response)

    except json.JSONDecodeError:
        print("Erro: A resposta da IA não é um JSON válido.")
        print("Resposta recebida:", response.text)
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao chamar a API do Gemini: {e}")
        return None

