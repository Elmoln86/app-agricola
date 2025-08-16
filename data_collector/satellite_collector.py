# Este é o arquivo: satellite_collector.py

import ee
import pandas as pd
import geemap

class SatelliteCollector:
    """
    Uma classe para coletar e processar dados de satélite usando a API
    do Google Earth Engine, focando em índices de vegetação como o NDVI.
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

    def get_ndvi_data(self):
        """
        Coleta dados de NDVI (Índice de Vegetação por Diferença Normalizada)
        de uma coleção de imagens do Earth Engine.
        """
        try:
            # Seleciona a coleção de imagens do Landsat 8
            collection = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
                          .filterDate(self.start_date, self.end_date)
                          .filterBounds(self.location)
                          .select('SR_B4', 'SR_B5')) # Seleciona as bandas Vermelha e NIR

            if collection.size().getInfo() == 0:
                print("Nenhuma imagem de satélite encontrada para a área e período selecionados.")
                return None

            # Calcula o NDVI
            def calculate_ndvi(image):
                return image.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')

            ndvi_collection = collection.map(calculate_ndvi)
            
            # Extrai o valor médio de NDVI na região
            mean_ndvi = ndvi_collection.mean().reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=self.location,
                scale=30 # Resolução em metros (30m para Landsat)
            ).getInfo()

            return mean_ndvi

        except Exception as e:
            print(f"Erro ao coletar dados de satélite: {e}")
            return None


if __name__ == '__main__':
    # Este é um exemplo de como testar a classe localmente
    
    # 1. Autentique e inicialize a API
    # ee.Authenticate()
    # ee.Initialize()
    
    # 2. Defina uma localização de exemplo (polígono de uma área de interesse)
    exemplo_location = ee.Geometry.Point([-47.9382, -15.7801]).buffer(1000)
    
    # 3. Crie uma instância da classe SatelliteCollector
    collector = SatelliteCollector('2024-01-01', '2024-01-31', exemplo_location)
    
    # 4. Chame o método para coletar os dados
    dados_satelite = collector.get_ndvi_data()
    
    if dados_satelite:
        print("\nDados de NDVI de exemplo coletados com sucesso:")
        print(dados_satelite)
