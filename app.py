# app.py
import streamlit as st
from backend_service import process_text_pipeline, process_image_pipeline # Importa as funções do backend

def main():
    st.set_page_config(layout="wide", page_title="ClarityFlow: Pipeline Detective")

    st.title("🔍 ClarityFlow: O Detetive de Pipelines")
    st.write("Faça upload de um arquivo de configuração de pipeline (JSON/YAML) ou de uma imagem para gerar o Data Lineage e a documentação.")

    st.markdown("---")

    # Escolha do tipo de input
    input_type = st.radio(
        "Selecione o tipo de input:",
        ("Arquivo de Configuração (JSON/YAML/TXT)", "Imagem da Pipeline"),
        key="input_type_radio"
    )

    uploaded_file = None
    if input_type == "Arquivo de Configuração (JSON/YAML/TXT)":
        uploaded_file = st.file_uploader(
            "Arraste e solte ou clique para fazer upload de um JSON/YAML/TXT",
            type=["json", "yaml", "yml", "txt"],
            key="text_file_uploader"
        )
    else: # Imagem da Pipeline
        uploaded_file = st.file_uploader(
            "Arraste e solte ou clique para fazer upload de uma imagem (PNG/JPG/JPEG)",
            type=["png", "jpg", "jpeg"],
            key="image_file_uploader"
        )

    # Botão de Processar
    process_button = st.button("Processar Pipeline", key="process_button")

    st.markdown("---")
    st.subheader("Resultados:")

    # Lógica de processamento só quando o botão é clicado E há um arquivo
    if process_button and uploaded_file is not None:
        with st.spinner("Processando... Por favor, aguarde. Isso pode levar alguns segundos..."):
            if input_type == "Arquivo de Configuração (JSON/YAML/TXT)":
                file_content = uploaded_file.getvalue().decode("utf-8")
                diagram_url, documentation_text = process_text_pipeline(file_content)
            else: # Imagem da Pipeline
                diagram_url, documentation_text = process_image_pipeline(uploaded_file)
            
            # Exibir os resultados reais (ou mocks)
            st.success("Processamento concluído!")
            
            # Usando st.tabs para organizar o diagrama e a documentação
            tab_diagram, tab_docs = st.tabs(["Diagrama de Linhagem", "Documentação"])
            
            with tab_diagram:
                st.image(diagram_url, caption="Diagrama de Linhagem Gerado")
                st.markdown(f"[Baixar Diagrama (PNG)](link_para_download_png) | [Baixar Diagrama (SVG)](link_para_download_svg)")

            with tab_docs:
                st.markdown(documentation_text)
                st.markdown(f"[Baixar Documentação (PDF/Markdown)](link_para_download_doc)")


    elif process_button and uploaded_file is None:
        st.warning("Por favor, faça upload de um arquivo antes de processar.")
    else:
        st.info("Aguardando o upload de um arquivo e o clique no botão 'Processar'.")

if __name__ == "__main__":
    main()

