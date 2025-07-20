import os
from google.cloud import vision

# Configura as credenciais automaticamente se você tiver o arquivo na raiz
# e o .gitignore configurado corretamente.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'gcp-credentials.json'

def get_text_from_image(content_bytes: bytes) -> str:
    """
    Usa a API do Google Cloud Vision para extrair texto de uma imagem.
    
    Args:
        content_bytes (bytes): O conteúdo da imagem em bytes.
        
    Returns:
        str: O texto completo extraído da imagem.
    """
    try:
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=content_bytes)
        
        # Realiza a detecção de texto no documento
        response = client.document_text_detection(image=image)
        
        if response.error.message:
            raise Exception(
                f'{response.error.message}\n'
                'Para mais informações, veja https://cloud.google.com/apis/design/errors'
            )
            
        return response.full_text_annotation.text
    except Exception as e:
        print(f"Erro ao processar imagem com a API do Cloud Vision: {e}")
        return None