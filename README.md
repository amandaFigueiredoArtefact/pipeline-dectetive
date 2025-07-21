# Arquitetura da Solução: Data Holmes

## 1. Visão Geral

A arquitetura do "Data Holmes" foi projetada de forma modular para garantir a separação de responsabilidades, facilidade de manutenção e a capacidade de estender a aplicação com novas funcionalidades no futuro. A solução é uma aplicação web interativa construída em Python, que utiliza um frontend reativo (Streamlit) e um backend desacoplado que orquestra a comunicação com serviços de Inteligência Artificial e bibliotecas de visualização.

O fluxo de dados começa na interface do usuário, passa por uma camada de orquestração no backend, é processado por serviços de IA especializados e, finalmente, é renderizado como um diagrama visual para o usuário.

## 2. Diagrama da Arquitetura

O diagrama abaixo ilustra os principais componentes da solução e como eles interagem entre si.

<img width="1215" height="272" alt="image" src="https://github.com/user-attachments/assets/2e157c7e-61ac-445b-ad4a-e46ceb43097a" />

## 3. Descrição dos Componentes

A solução é dividida nas seguintes camadas e componentes lógicos:

#### a. Frontend (Interface do Usuário - **`app.py`**)

* **Tecnologia:** Streamlit
* **Responsabilidade:** É a única camada com a qual o usuário interage diretamente. É responsável por:
    * Apresentar os widgets de entrada (seleção de IA, upload de ficheiros, área de texto).
    * Capturar as entradas do usuário (o ficheiro, o texto colado, a escolha da IA).
    * Chamar a camada de orquestração do backend quando o usuário clica no botão "Gerar".
    * Exibir os resultados finais (o diagrama de linhagem e o dicionário de dados) que são retornados pelo backend.

#### b. Backend (Camada de Lógica)

O backend é composto por módulos Python distintos, cada um com uma responsabilidade clara.

* **Orquestrador (`lineage_creator.py` e `catalog_creator.py`):**
    * **Responsabilidade:** Atua como o "cérebro" da aplicação. Recebe as solicitações do frontend, decide qual prompt de IA usar com base no tipo de ficheiro, chama os serviços necessários (OCR e IA) e passa o resultado estruturado para o visualizador.
* **Cliente de IA (`ai_client.py`):**
    * **Responsabilidade:** Abstrai toda a complexidade da comunicação com as APIs de IA. Contém as funções para se conectar ao Google Gemini e ao OpenAI ChatGPT, enviar os prompts e tratar as respostas, garantindo que elas retornem no formato esperado (JSON).
* **Processador de Imagem (`ocr_processor.py`):**
    * **Responsabilidade:** Módulo especializado que lida exclusivamente com as entradas de imagem. Ele recebe os bytes da imagem do orquestrador e os envia para a API do Google Cloud Vision para realizar o OCR e retornar o texto extraído.
* **Visualizador (`visualizer.py`):**
    * **Responsabilidade:** É o componente responsável pela geração dos outputs visuais. Utiliza a biblioteca **Graphviz** para pegar os dados JSON estruturados (com `nodes` e `edges`) retornados pela IA e desenhar os diagramas de linhagem de dados ou os diagramas entidade-relacionamento.

#### c. Serviços Externos e Bibliotecas

* **APIs de IA (Google Gemini & OpenAI ChatGPT):** São os serviços externos que fornecem a inteligência para interpretar o conteúdo dos ficheiros e extrair a estrutura de dados.
* **API de OCR (Google Cloud Vision):** Serviço externo utilizado para "ler" o texto de ficheiros de imagem.
* **Graphviz:** Biblioteca open-source fundamental que é utilizada pelo `visualizer.py` para renderizar os gráficos e diagramas de forma programática.

## 1. Testar aplicação

* **Para rodar a aplicação execute : `streamlit run app.py` , se esse nao funcionar tente com `python -m streamlit run app.py`.**
  
