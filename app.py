import streamlit as st
import os # Importamos a biblioteca 'os' para trabalhar com nomes de ficheiros
from backend.lineage_creator import generate_from_content

# --- Configuração da Página ---
st.set_page_config(
    page_title="Data Holmes",
    page_icon="🕵️",
    layout="centered"
)

# --- Inicialização do Session State ---
if 'generated_image_path' not in st.session_state:
    st.session_state.generated_image_path = None

# --- Título e Descrição ---
st.title("🕵️ Data Holmes")
st.write("Analise a linhagem de dados de pipelines a partir de arquivos, imagens ou texto colado.")
st.divider()

# --- Lógica de Callbacks ---
def run_analysis(content, file_type, ai_provider):
    spinner_message = f"Analisando texto com {ai_provider}..."
    if file_type in ['png', 'jpg', 'jpeg']:
        spinner_message = f"Analisando imagem com {ai_provider}... O OCR pode demorar um pouco."

    with st.spinner(spinner_message):
        try:
            st.session_state.generated_image_path = generate_from_content(
                content_bytes=content, 
                file_type=file_type, 
                ai_provider=ai_provider
            )
        except Exception as e:
            st.error(f"Ocorreu um erro crítico durante o processamento: {e}")
            st.session_state.generated_image_path = None


# --- PARTE 1: COLETANDO OS INPUTS DO USUÁRIO ---
selected_ai = st.selectbox(
    "**Passo 1: Escolha o modelo de IA para a análise:**",
    ('Gemini', 'ChatGPT'),
    help="Modelos diferentes podem gerar resultados e velocidades distintas."
)

st.write("**Passo 2: Forneça os dados da sua pipeline:**")
tab1, tab2 = st.tabs(["📤 Enviar Arquivo", "📋 Colar Texto"])

content_to_pass = None
file_type = ""

with tab1:
    uploaded_file = st.file_uploader(
        "Envie um arquivo",
        type=['json', 'sql', 'yml', 'yaml', 'png', 'jpg', 'jpeg'],
        label_visibility="collapsed"
    )
    if uploaded_file:
        # --- LÓGICA DE DETECÇÃO DE TIPO CORRIGIDA ---
        # Usamos a extensão do nome do ficheiro, que é mais fiável.
        file_extension = os.path.splitext(uploaded_file.name)[1].lower().replace('.', '')
        file_type = file_extension
        content_to_pass = uploaded_file.getvalue()
        st.info(f"Arquivo '{uploaded_file.name}' pronto para análise (tipo detectado: {file_type}).")

with tab2:
    text_input = st.text_area(
        "Cole o conteúdo de texto aqui",
        height=250,
        placeholder="""Exemplo de SQL:\n\nCREATE TABLE A as SELECT * FROM B JOIN C ON B.id = C.id;"""
    )
    file_type_from_radio = st.radio(
        "Confirme o tipo do conteúdo colado:",
        ('json', 'sql', 'yaml'),
        horizontal=True,
        key='content_type_radio'
    )
    if not uploaded_file and text_input:
        file_type = file_type_from_radio
        content_to_pass = text_input.encode("utf-8")

st.divider()

# --- PARTE 2: BOTÕES DE AÇÃO ---
col1, col2 = st.columns(2)

with col1:
    if st.button("Gerar Linhagem de Dados ✨", use_container_width=True, type="primary"):
        if content_to_pass:
            run_analysis(content_to_pass, file_type, selected_ai)
        else:
            st.warning("Por favor, envie um arquivo ou cole um conteúdo de texto.")


# --- PARTE 3: EXIBIÇÃO DO RESULTADO ---
if st.session_state.generated_image_path:
    st.success("Linhagem de dados gerada com sucesso!")
    st.image(st.session_state.generated_image_path, caption=f"Diagrama gerado por {selected_ai}")
    
    with open(st.session_state.generated_image_path, "rb") as file:
        st.download_button(
            label="Baixar Diagrama (PNG)",
            data=file,
            file_name="data_lineage.png",
            mime="image/png"
        )
elif st.session_state.generated_image_path is None and 'button' in st.session_state and st.session_state.button:
    st.error("Ocorreu uma falha no backend. A IA não conseguiu processar o conteúdo. Verifique o terminal para mais detalhes.")
