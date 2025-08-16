import streamlit as st
import pandas as pd
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Importações dos seus módulos personalizados
from data_collector.weather_collector import DataCollector
from data_collector.satellite_collector import SatelliteCollector
from data_collector.financial_collector import FinancialCollector
from ia_engine.training import Trainer
from ia_engine.predict import Predictor
from ia_engine.llm_chatbot import Chatbot
from automation.irrigation_controller import IrrigationController
from digital_twin.visualization import DigitalTwin

# --- LÓGICA DE CRIAÇÃO DE ARQUIVOS INICIAIS ---
def create_initial_files():
    """
    Verifica se a pasta de modelos e arquivos de exemplo existem.
    Caso não existam, cria-os com dados básicos para a primeira execução.
    """
    # 1. Cria a pasta para o modelo, se não existir
    model_dir = "ia_engine/models"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # 2. Cria um modelo básico e o salva, se o arquivo não existir
    model_path = os.path.join(model_dir, "productivity_model.h5")
    if not os.path.exists(model_path):
        st.warning("Modelo de produtividade não encontrado. Treinando e criando um modelo inicial...")
        # Lógica para criar um modelo simples (um placeholder)
        model = Sequential([
            Dense(32, activation='relu', input_shape=(4,)),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        # Simula o salvamento
        model.save(model_path)
        st.success("Modelo inicial criado com sucesso!")

    # 3. Cria um arquivo de dados de exemplo, se não existir
    data_dir = "digital_twin"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    data_path = os.path.join(data_dir, "dados_exemplo.csv")
    if not os.path.exists(data_path):
        st.warning("Dados de exemplo não encontrados. Criando um arquivo de dados inicial...")
        # Cria um DataFrame de exemplo
        dummy_data = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [1, 2, 3, 4, 5],
            'z': [10, 11, 9, 12, 10],
            'saude': [0.8, 0.9, 0.7, 0.95, 0.85]
        })
        dummy_data.to_csv(data_path, index=False)
        st.success("Arquivo de dados de exemplo criado com sucesso!")

# --- INÍCIO DO APLICATIVO ---
st.title("Agri-IA Conilon: Otimização Inteligente de Cultivo")

# Executa a função de verificação e criação de arquivos
create_initial_files()

# --- Instâncias dos módulos ---
collector = DataCollector()
sat_collector = SatelliteCollector()
financial_collector = FinancialCollector()
predictor = Predictor()
irrigation_controller = IrrigationController()
digital_twin = DigitalTwin()
chatbot = Chatbot(predictor)

# --- Seção de Coleta de Dados e Entrada do Usuário ---
with st.sidebar:
    st.header("Entrada de Dados")
    lat = st.number_input("Latitude", value=-20.27, format="%.2f")
    lon = st.number_input("Longitude", value=-40.30, format="%.2f")
    
    st.subheader("Dados Históricos (Opcional)")
    uploaded_history = st.file_uploader("Envie um arquivo CSV com histórico da lavoura", type="csv")
    
    st.subheader("Análise de Solo Manual")
    with st.expander("Informar dados de análise de solo"):
        st.write("Insira os valores da sua análise de solo para uma previsão mais precisa.")
        ph_value = st.number_input("pH do Solo", min_value=1.0, max_value=14.0, value=6.0)
        nitrogen_value = st.number_input("Nitrogênio (N) em mg/dm³", min_value=0.0, value=30.0)
        fosforo_value = st.number_input("Fósforo (P) em mg/dm³", min_value=0.0, value=15.0)
        potassio_value = st.number_input("Potássio (K) em mg/dm³", min_value=0.0, value=80.0)
    
    st.write("---")
    st.subheader("Upload de Imagens")
    uploaded_file = st.file_uploader("Envie uma foto da planta para diagnóstico")

# --- Botão principal para iniciar a análise ---
if st.button("Buscar Dados e Gerar Análise"):
    st.header("Análise e Recomendações")
    
    if uploaded_history is not None:
        historical_data = pd.read_csv(uploaded_history)
        st.success("Dados históricos carregados com sucesso!")
    else:
        st.info("Nenhum dado histórico carregado. Usando dados da internet para a análise.")
        historical_data = pd.DataFrame()
    
    soil_data = {
        'pH': ph_value,
        'nitrogenio': nitrogen_value,
        'fosforo': fosforo_value,
        'potassio': potassio_value
    }
    st.write("Análise de solo informada:", soil_data)
    
    st.subheader("Dados Climáticos Atuais")
    weather_data = collector.get_weather_data(lat, lon)
    st.json(weather_data) 
    
    st.subheader("Plano de Manejo")
    plan = predictor.generate_irrigation_plan(soil_data, weather_data) 
    st.info(plan)
    
    st.subheader("Previsão de Produtividade")
    productivity_prediction = predictor.predict_productivity(historical_data, weather_data, soil_data)
    st.success(f"Previsão de produtividade para a próxima safra: {productivity_prediction} sacas/ha.")

if uploaded_file is not None:
    st.header("Diagnóstico de Pragas e Doenças")
    # ... (lógica de diagnóstico existente) ...

# --- Seção de Otimização Financeira ---
st.header("Otimização Econômica")
if st.button("Buscar Preços Futuros do Café"):
    prices = financial_collector.get_coffee_prices()
    st.subheader("Preços do Café (Último Mês)")
    st.line_chart(prices)

# --- Seção de Assistente de IA (Chatbot) ---
st.header("Assistente de IA")
st.write("Pergunte sobre a sua lavoura. Ex: 'Qual a previsão de produtividade?'")
user_input = st.text_input("Sua pergunta:")

if user_input:
    context_data = {
        'sensor': {'umidade_solo': 25},
        'weather': {'precipitacao': 0},
        'historical': pd.DataFrame(),
        'satellite': {'ndvi_value': 0.85}
    }
    
    response = chatbot.get_response(user_input, context_data)
    st.info(response)

# --- Seção de Automação ---
st.header("Controle de Automação")
st.write("Dispare comandos inteligentes para o seu equipamento.")
zone_id = st.text_input("ID da Zona de Irrigação:", value="talhao_3")
amount_mm = st.number_input("Quantidade de água (mm):", value=10.0)

if st.button("Disparar Irrigação"):
    result = irrigation_controller.send_command(zone_id, amount_mm)
    if result['status'] == 'success':
        st.success(f"Comando de irrigação de {amount_mm}mm enviado para o talhão {zone_id}!")
    else:
        st.error(f"Erro: {result['message']}")
