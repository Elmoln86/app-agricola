import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
import pandas as pd
import numpy as np

class Trainer:
    def __init__(self):
        self.model = None

    def train_productivity_model(self, historical_data):
        """
        Treina um modelo de regressão para prever a produtividade.
        
        Args:
            historical_data (DataFrame): DataFrame com dados históricos de clima, solo e produtividade.
        """
        # Preparação dos dados
        X = historical_data[['umidade', 'temp', 'ndvi_medio']].values
        y = historical_data['produtividade'].values

        # Criação do modelo (um modelo simples de rede neural)
        self.model = Sequential([
            Dense(64, activation='relu', input_shape=(X.shape[1],)),
            Dense(32, activation='relu'),
            Dense(1)  # Camada de saída para regressão
        ])

        # Compilação e treinamento
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        self.model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2)

        # Salva o modelo treinado
        self.model.save('ia_engine/models/productivity_model.h5')
        print("Modelo de produtividade treinado e salvo com sucesso!")

    def train_disease_detection_model(self, image_dataset):
        """
        Treina um modelo de classificação para detectar doenças em imagens.
        
        Args:
            image_dataset (tf.data.Dataset): Dataset de imagens e rótulos para treinamento.
        """
        # Criação de um modelo CNN (Rede Neural Convolucional)
        self.model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dense(1, activation='sigmoid') # Para classificação binária (doença/saudável)
        ])

        # Compilação e treinamento
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.model.fit(image_dataset, epochs=10)

        # Salva o modelo treinado
        self.model.save('ia_engine/models/disease_detection_model.h5')
        print("Modelo de detecção de doenças treinado e salvo com sucesso!")
