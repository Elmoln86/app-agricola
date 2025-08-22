rt streamlit as st
import ee
import json
import os
from data_collector.weather_collector import DataCollector
from data_collector.satellite_collector import SatelliteCollector
from data_collector.financial_collector import FinancialCollector
from ia_engine.training import Trainer
from ia_engine.predict import Predictor
from ia_engine.llm_chatbot import Chatbot
from automation.irrigation_controller import IrrigationController
from digital_twin.visualization import DigitalTwin

# --- Configurações da Página Streamlit ---
st.set_page_config(layout="wide", page_title="App Agrícola Inteligente")
st.title("Plataforma de Gestão Agrícola Inteligente")
st.markdown("Bem-vindo à sua plataforma integrada de análise e automação agrícola.")

# --- Autenticação e Inicialização da API do Google Earth Engine ---
# Este bloco de código agora forçará a autenticação usando o JSON do arquivo secrets.toml
try:
    st.header("Status da Autenticação do Google Earth Engine")

    # Tenta obter as credenciais do Streamlit secrets
    creds_json = st.secrets["gee_credentials"]["private_key_json"]

    # Se a chave for uma string, parseia para JSON
    if isinstance(creds_json, str):
        creds_json = json.loads(creds_json)

    # Autentica diretamente usando as credenciais do JSON
    ee.Authenticate(credentials=ee.ServiceAccountCredentials(
        creds_json["client_email"],
        creds_json["private_key"]
    ))
    
    # Inicializa a API
    ee.Initialize()

    st.success("🎉 A autenticação com o Google Earth Engine foi bem-sucedida! 🎉")
    st.write("Isso significa que suas credenciais estão funcionando e as permissões foram concedidas.")
    
    # Exemplo de teste simples para confirmar a conexão
    st.header("Teste de Conexão com a API")
    try:
        location = ee.Geometry.Point([-47.9382, -15.7801])
        st.write("Conexão com o Earth Engine estabelecida com sucesso!")
        st.write(f"Geometria de teste: {location.getInfo()}")
    except ee.EEException as e:
        st.error(f"Erro ao executar o teste da API. O problema ainda pode ser na sua conta. Erro: {e}")

except Exception as e:
    st.error("❌ Erro ao inicializar o Google Earth Engine. ❌")
    st.write("Ocorreu um problema com a autenticação. Por favor, verifique os seguintes pontos:")
    st.markdown("- Suas credenciais no arquivo `secrets.toml` estão formatadas corretamente.")
    st.markdown("- Sua conta de serviço tem as permissões necessárias no seu projeto do Google Cloud e no Google Earth Engine.")
    st.markdown("- A chave privada no seu `secrets.toml` está correta e não tem caracteres extra.")
    st.markdown(f"**Detalhes do erro:** {e}")
    st.stop()


# --- Instâncias dos Módulos com Argumentos ---
start_date_exemplo = '2024-01-01'
end_date_exemplo = '2024-01-31'
location_exemplo = ee.Geometry.Point([-47.9382, -15.7801])

# Instanciando as classes com os argumentos corretos
weather_collector = DataCollector(start_date=start_date_exemplo, end_date=end_date_exemplo, location=location_exemplo)
satellite_collector = SatelliteCollector(start_date=start_date_exemplo, end_date=end_date_exemplo, location=location_exemplo)
financial_collector = FinancialCollector()
trainer = Trainer()
predictor = Predictor(model=None)
chatbot = Chatbot()
irrigation_controller = IrrigationController()
digital_twin = DigitalTwin()

# --- Lógica da Aplicação ---

# Exemplo de como usar o DataCollector
st.header("Dados Meteorológicos")
if st.button("Coletar Dados Meteorológicos"):
    with st.spinner('Coletando dados...'):
        dados_tempo = weather_collector.get_weather_data()
        if dados_tempo is not None:
            st.success("Dados de tempo coletados com sucesso!")
            st.dataframe(dados_tempo.head())
        else:
            st.error("Não foi possível coletar os dados de tempo.")

# Exemplo de como usar o SatelliteCollector
st.header("Análise de Satélite (NDVI)")
if st.button("Coletar Dados de Satélite"):
    with st.spinner('Coletando dados...'):
        dados_satelite = satellite_collector.get_ndvi_data()
        if dados_satelite is not None:
            st.success("Dados de satélite coletados com sucesso!")
            st.write(dados_satelite)
        else:
            st.error("Não foi possível coletar os dados de satélite.")
