# Este é o arquivo: weather_collector.py

import ee
import pandas as pd
import geemap

class DataCollector:
    """
    Uma classe para coletar e processar dados meteorológicos e de satélite
    usando a API do Google Earth Engine.
    """

    def __init__(self, start_date, end_date, location):
        """
        Inicializa o coletor de dados com o intervalo de datas e a localização.
        
        Args:
            start_date (str): Data de início no formato 'YYYY-MM-DD'.
            end_date (str): Data de fim no formato 'YYYY-MM-DD'.
            location (ee.Geometry.Point ou ee.Geometry.Polygon): Geometria da área de interesse.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.location = location

    def get_weather_data(self):
        """
        Coleta dados de precipitação e temperatura de uma coleção de dados
        do Earth Engine.
        """
        try:
            # AQUI ESTÁ A CORREÇÃO: ee.Initialize()
            ee.Initialize()
            
            # Seleciona uma coleção de dados de clima (ex: CHIRPS para precipitação)
            collection = (ee.ImageCollection('NOAA/CFSR')
                          .filterDate(self.start_date, self.end_date)
                          .filterBounds(self.location))

            if collection.size().getInfo() == 0:
                print("Nenhum dado encontrado para a área e período selecionados.")
                return None

            # Converte a coleção para um objeto GeoPandas para visualização ou análise
            # A conversão para o lado do cliente (getInfo()) pode ser lenta para grandes conjuntos de dados
            
            # Exemplo de como extrair valores médios de uma banda específica
            mean_temp = collection.select('TMP_2m').mean().reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=self.location,
                scale=1000 # Escala em metros
            ).getInfo()

            return mean_temp

        except Exception as e:
            print(f"Erro ao coletar dados do Earth Engine: {e}")
            return None


if __name__ == '__main__':
    # Este é um exemplo de como testar a classe localmente
    
    # 1. Autentique e inicialize a API (se estiver rodando no seu ambiente local)
    # ee.Authenticate()
    # ee.Initialize()
    
    # 2. Defina uma localização de exemplo (ponto em coordenadas lat/lon)
    exemplo_location = ee.Geometry.Point([-47.9382, -15.7801])
    
    # 3. Crie uma instância da classe DataCollector
    collector = DataCollector('2024-01-01', '2024-01-31', exemplo_location)
    
    # 4. Chame o método para coletar os dados
    dados_clima = collector.get_weather_data()
    
    if dados_clima:
        print("\nDados de exemplo coletados com sucesso:")
        print(dados_clima)
