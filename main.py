import streamlit as st
import ee
import json

st.set_page_config(
    page_title="Plataforma de Gestão Agrícola Inteligente",
    layout="wide"
)

# Título da aplicação
st.title("Plataforma de Gestão Agrícola Inteligente")
st.write("Bem-vindo à sua plataforma integrada de análise e automação agrícola.")

st.divider()

# Iniciar o Google Earth Engine
st.header("Status da Autenticação do Google Earth Engine")
st.info("A tentar autenticar com o Google Earth Engine...")

try:
    # 1. Carregar as credenciais do Streamlit secrets
    # Acessar a chave 'EE_CREDENTIALS' definida no secrets.toml
    if 'EE_CREDENTIALS' in st.secrets:
        # Pega a string JSON do segredo
        credentials_json = st.secrets["EE_CREDENTIALS"]
        
        # O Streamlit já carrega o TOML como um dicionário, então podemos
        # tentar aceder diretamente aos dados, ou decodificar a string JSON se
        # ela for tratada como tal. A primeira abordagem é mais robusta.
        # Se for um TOML simples, a chave pode ser acessada diretamente
        # Se for uma string JSON, decodifique-a
        if isinstance(credentials_json, str):
            credentials_dict = json.loads(credentials_json)
        else:
            credentials_dict = credentials_json
            
        # 2. Inicializar o Google Earth Engine com as credenciais
        ee.Initialize(credentials=ee.ServiceAccountCredentials(
            credentials_dict['client_email'],
            credentials_dict['private_key']
        ))
        
        st.success("Autenticação com o Google Earth Engine concluída com sucesso!")
        st.write("Agora pode começar a usar as funcionalidades do Earth Engine.")
    else:
        st.error("Chave 'EE_CREDENTIALS' não encontrada nos segredos do Streamlit.")
        st.warning("Por favor, adicione as suas credenciais de conta de serviço do Google Earth Engine.")
        st.warning("Nas definições da sua aplicação no Streamlit Cloud, adicione um 'Secret' com a chave 'EE_CREDENTIALS' e o valor como o conteúdo do seu ficheiro JSON.")

except Exception as e:
    st.error(f"Ocorreu um erro ao inicializar o Google Earth Engine: {e}")
    st.info("Ocorreu um problema com a autenticação. Por favor, verifique os seguintes pontos:")
    st.info("- As suas credenciais estão no formato JSON correto.")
    st.info("- A sua conta de serviço tem as permissões necessárias no seu projeto do Google Cloud e no Google Earth Engine.")
    st.info("- O 'Secret' no Streamlit Cloud foi adicionado e formatado corretamente.")

# Exemplo de funcionalidade do Earth Engine (apenas para verificação)
try:
    # Este exemplo usa ee.Image() para confirmar a conexão
    st.header("Exemplo de Conexão com o Earth Engine")
    st.write("A carregar uma imagem de exemplo do Earth Engine para testar a conexão.")
    
    # Tente carregar uma imagem e imprimir a sua projeção.
    # Se a autenticação falhar, esta linha irá levantar uma exceção.
    landsat_image = ee.Image('LANDSAT/LC08/C01/T1_SR/LC08_044034_20140318')
    st.write("Imagem Landsat carregada com sucesso!")
    
except Exception as e:
    st.warning(f"Não foi possível carregar a imagem de exemplo. Erro: {e}")
    st.write("Isto pode acontecer se a autenticação falhou. Por favor, verifique o seu arquivo `secrets.toml`.")

