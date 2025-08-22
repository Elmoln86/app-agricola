import streamlit as st
import ee
import json
import os
import toml

# Tentar carregar os segredos a partir do ficheiro toml manualmente, se st.secrets falhar.
def load_secrets_manually():
    """
    Tenta carregar os segredos do ficheiro secrets.toml.
    Isto é uma solução alternativa se st.secrets não funcionar como esperado.
    """
    secrets_path = ".streamlit/secrets.toml"
    if os.path.exists(secrets_path):
        try:
            with open(secrets_path, "r") as f:
                secrets = toml.load(f)
                return secrets
        except Exception as e:
            st.error(f"Erro ao ler o ficheiro secrets.toml manualmente: {e}")
    return {}

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
    # 1. Carregar as credenciais. Tentar primeiro com st.secrets
    credentials_source = None
    if 'EE_CREDENTIALS' in st.secrets:
        credentials_json = st.secrets["EE_CREDENTIALS"]
        credentials_source = "st.secrets"
    else:
        # Se st.secrets falhar, tentar a abordagem manual
        manual_secrets = load_secrets_manually()
        if 'EE_CREDENTIALS' in manual_secrets:
            credentials_json = manual_secrets["EE_CREDENTIALS"]
            credentials_source = "manual"
        else:
            st.error("Chave 'EE_CREDENTIALS' não encontrada nos segredos do Streamlit.")
            st.warning("Por favor, adicione as suas credenciais de conta de serviço do Google Earth Engine.")
            st.warning("Nas definições da sua aplicação no Streamlit Cloud, adicione um 'Secret' com a chave 'EE_CREDENTIALS' e o valor como o conteúdo do seu ficheiro JSON.")
            st.stop() # Parar a execução se as credenciais não forem encontradas

    # 2. Decodificar a string JSON e inicializar o Earth Engine
    if isinstance(credentials_json, str):
        credentials_dict = json.loads(credentials_json)
    else:
        credentials_dict = credentials_json

    ee.Initialize(credentials=ee.ServiceAccountCredentials(
        credentials_dict['client_email'],
        credentials_dict['private_key']
    ))
    
    st.success(f"Autenticação com o Google Earth Engine concluída com sucesso! (Fonte: {credentials_source})")
    st.write("Agora pode começar a usar as funcionalidades do Earth Engine.")

except Exception as e:
    st.error(f"Ocorreu um erro ao inicializar o Google Earth Engine: {e}")
    st.info("Ocorreu um problema com a autenticação. Por favor, verifique os seguintes pontos:")
    st.info("- As suas credenciais estão no formato JSON correto.")
    st.info("- A sua conta de serviço tem as permissões necessárias no seu projeto do Google Cloud e no Google Earth Engine.")
    st.info("- O 'Secret' no Streamlit Cloud foi adicionado e formatado corretamente.")
    st.info("Caso o erro persista, verifique se o ficheiro `secrets.toml` está no diretório `.streamlit`.")

st.divider()

# Exemplo de funcionalidade do Earth Engine (apenas para verificação)
st.header("Exemplo de Conexão com o Earth Engine")
st.write("A carregar uma imagem de exemplo do Earth Engine para testar a conexão.")
try:
    # Tente carregar uma imagem e imprimir a sua projeção.
    landsat_image = ee.Image('LANDSAT/LC08/C01/T1_SR/LC08_044034_20140318')
    st.write("Imagem Landsat carregada com sucesso!")
    
except Exception as e:
    st.warning(f"Não foi possível carregar a imagem de exemplo. Erro: {e}")
    st.write("Isto pode acontecer se a autenticação falhou. Por favor, verifique o seu arquivo `secrets.toml`.")

