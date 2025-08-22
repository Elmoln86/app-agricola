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
import json
import os

# --- Configurações da Página Streamlit ---
st.set_page_config(layout="wide", page_title="App Agrícola Inteligente")
st.title("Plataforma de Gestão Agrícola Inteligente")
st.markdown("Bem-vindo à sua plataforma integrada de análise e automação agrícola.")


# --- Autenticação e Inicialização da API do Google Earth Engine ---
try:
    # A única forma de fazer isso funcionar no Streamlit Cloud é
    # usando chaves planas e inicializando com as credenciais lidas.
    
    # Ler a chave privada e o email do secrets.toml
    # Assumimos que a chave privada está em uma única linha,
    # por isso a correção no código para adicionar as quebras de linha.
    private_key = st.secrets["earthengine_private_key"]
    client_email = st.secrets["earthengine_client_email"]
    
    # Reconstruir a chave privada com as quebras de linha corretas
    private_key_multiline = private_key.replace("-----BEGIN PRIVATE KEY-----", "-----BEGIN PRIVATE KEY-----\n")
    private_key_multiline = private_key_multiline.replace("-----END PRIVATE KEY-----", "\n-----END PRIVATE KEY-----")
    
    # Substitui espaços por quebras de linha para formatar corretamente a chave
    lines = private_key_multiline.split(" ")
    private_key_multiline_final = "-----BEGIN PRIVATE KEY-----\n" + "\n".join(lines[1:-1]) + "\n-----END PRIVATE KEY-----"

    # Inicializar o Earth Engine com as credenciais lidas
    ee.Initialize(
        credentials=ee.ServiceAccountCredentials(
            client_email,
            private_key_multiline_final
        )
    )
    st.success("🎉 A autenticação com o Google Earth Engine foi bem-sucedida! 🎉")
    st.write("Isso significa que suas credenciais e conta estão corretas.")

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
    st.markdown("- Suas credenciais no arquivo `secrets.toml` estão corretas.")
    st.markdown("- Sua conta Google foi aprovada para usar o Earth Engine.")
    st.markdown(f"**Detalhes do erro:** {e}")

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
