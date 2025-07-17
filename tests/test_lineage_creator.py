# tests/test_lineage_creator.py

import os
import sys

# Garante que o script consegue achar a pasta 'backend'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.lineage_creator import generate_from_content

def run_tests():
    """
    Função principal que executa todos os testes automatizados.
    """
    print("--- INICIANDO TESTES AUTOMATIZADOS DO BACKEND ---")

    # Pega o caminho do diretório onde este script de teste está
    script_dir = os.path.dirname(__file__) 
    
    # --- PONTO DE ATENÇÃO ---
    # Verifique se os nomes dos arquivos aqui batem EXATAMENTE com os nomes na pasta tests/test_data/
    test_files = {
        "json": os.path.join(script_dir, "test_data", "pipeline_exemplo.json"), # <--- VERIFIQUE ESTE NOME
        "sql": os.path.join(script_dir, "test_data", "script_exemplo.sql")
    }
    
    for file_type, file_path in test_files.items():
        print(f"\n--- Testando arquivo do tipo: {file_type.upper()} ---")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"ERRO: Arquivo de teste não encontrado em '{os.path.abspath(file_path)}'")
            continue

        print(f"\n>>> Executando com o provedor: GEMINI")
        
        try:
            # --- CORREÇÃO DO 'TypeError' ---
            # A chamada da função agora está mais simples, sem o 'ai_provider'.
            image_path = generate_from_content(
                content=content,
                file_type=file_type
            )

            if image_path and os.path.exists(image_path):
                print(f"✅ SUCESSO: Diagrama gerado e salvo em '{image_path}'")
            else:
                print(f"❌ FALHA: A função não retornou um caminho de imagem válido.")

        except Exception as e:
            print(f"❌ ERRO CRÍTICO ao testar com GEMINI: {e}")

    print("\n--- TESTES AUTOMATIZADOS CONCLUÍDOS ---")

if __name__ == "__main__":
    run_tests()