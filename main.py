import streamlit as st
import ee
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
# O erro estava aqui. A sua conta é do tipo 'authorized_user' (usuário autorizado),
# e a função `ee.ServiceAccountCredentials` é para 'service account' (conta de serviço).
# A forma correta de inicializar com suas credenciais é usando `ee.Initialize()`
# sem argumentos. A biblioteca do Earth Engine é inteligente o suficiente para
# encontrar as credenciais no arquivo .streamlit/secrets.toml por conta própria.
try:
    ee.Initialize()
    st.success("Google Earth Engine inicializado com sucesso!")
except Exception as e:
    st.error(f"Erro ao inicializar o Google Earth Engine. Verifique as credenciais. Erro: {e}")


# --- Instâncias dos Módulos com Argumentos ---
# Para resolver o TypeError, passamos valores de exemplo para os inicializadores das classes.
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


# ... adicione outras seções para os outros módulos ...
# (financeiro, predição, chatbot, irrigação)
