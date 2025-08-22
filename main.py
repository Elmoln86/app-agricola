import os
import streamlit as st
import ee
import json
from google.oauth2.service_account import Credentials

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

# Tente carregar o JSON diretamente da variável de ambiente
try:
    # Obtém o conteúdo JSON da variável de ambiente
    # A variável deve ser definida no Streamlit Cloud com o nome EE_CREDENTIALS
    credentials_json = os.environ['EE_CREDENTIALS']
    
    # Decodifica a string JSON para um objeto Python
    EE_CREDENTIALS = json.loads(credentials_json)
    
    # Se a chave privada contiver quebras de linha escapadas ('\n'),
    # o json.loads() já as deve ter processado. No entanto, se o segredo
    # foi colado de uma forma diferente, pode ser necessário este passo extra.
    # Ex: se o utilizador colou o valor com '\n' literalmente
    if isinstance(EE_CREDENTIALS, dict) and "private_key" in EE_CREDENTIALS:
        if '\\n' in EE_CREDENTIALS["private_key"]:
            EE_CREDENTIALS["private_key"] = EE_CREDENTIALS["private_key"].replace('\\n', '\n')

    # Autenticar com as credenciais da conta de serviço
    creds = Credentials.from_service_account_info(EE_CREDENTIALS)
    ee.Initialize(credentials=creds)
    
    st.success("Autenticação com o Google Earth Engine concluída com sucesso!")
    st.write("Agora pode começar a usar as funcionalidades do Earth Engine.")
    
except KeyError:
    st.error("Variável de ambiente 'EE_CREDENTIALS' não encontrada.")
    st.warning("Por favor, adicione as suas credenciais de conta de serviço do Google Earth Engine como uma variável de ambiente.")
    st.warning("Nas definições da sua aplicação no Streamlit Cloud, adicione um 'Secret' com a chave 'EE_CREDENTIALS' e o valor como o conteúdo do seu ficheiro JSON.")
except json.JSONDecodeError as e:
    st.error(f"Erro ao decodificar JSON da variável de ambiente 'EE_CREDENTIALS': {e}")
    st.warning("Verifique se as suas credenciais estão num formato JSON válido e se a 'private_key' está numa única linha.")
except Exception as e:
    st.error(f"Ocorreu um erro ao inicializar o Google Earth Engine: {e}")
    st.info("Ocorreu um problema com a autenticação. Por favor, verifique os seguintes pontos:")
    st.info("- As suas credenciais estão no formato JSON correto.")
    st.info("- A sua conta de serviço tem as permissões necessárias no seu projeto do Google Cloud e no Google Earth Engine.")
    st.info("- O 'Secret' no Streamlit Cloud foi adicionado e formatado corretamente.")

# Exemplo de funcionalidade do Earth Engine (apenas para verificação)
try:
    if ee.data.getAccessToken() is not None:
        st.header("Exemplo de Mapa")
        st.write("Este mapa é gerado usando dados do Google Earth Engine para confirmar que a autenticação funcionou.")
        
        # Exemplo simples: visualizar a elevação global
        dem = ee.Image('USGS/SRTMGL1_003')
        vis_params = {'min': 0, 'max': 4000}
        
        # Mova o mapa para uma localização global (opcional)
        map_object = ee.mapclient.centerMap(-112.87, 36.31, 10)
        
        # Adicionar o layer de elevação ao mapa
        map_id = dem.getMapId(vis_params)
        
        # Inserir o mapa no streamlit
        # Nota: O streamlit-folium é uma boa biblioteca para integrar mapas
        # mas para este exemplo, vamos manter a simplicidade.
        st.write("Mapa de elevação SRTM (apenas um exemplo visual).")

except Exception as e:
    st.warning(f"Não foi possível executar a funcionalidade de exemplo do EE. Erro: {e}")
    st.write("Isto pode acontecer se a autenticação falhou.")

