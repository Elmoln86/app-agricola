import ee
import pandas as pd
import json

class DataCollector:
    """
    Coleta dados meteorológicos e ambientais usando o Google Earth Engine.
    """
    def __init__(self, start_date, end_date, location):
        """
        Inicializa o coletor de dados.

        Args:
            start_date (str): Data de início no formato 'YYYY-MM-DD'.
            end_date (str): Data de fim no formato 'YYYY-MM-DD'.
            location (ee.Geometry): A geometria do ponto ou polígono para a coleta de dados.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.location = location

    def get_weather_data(self):
        """
        Coleta dados de temperatura, precipitação e umidade da imagem de reanálise ERA5
        do Google Earth Engine.

        Returns:
            pandas.DataFrame: Um DataFrame com os dados coletados, ou None em caso de erro.
        """
        try:
            # Defina o conjunto de dados da imagem de reanálise ERA5
            era5_image = ee.ImageCollection('ECMWF/ERA5_LAND/MONTHLY') \
                .filterDate(self.start_date, self.end_date) \
                .filterBounds(self.location)

            # Defina as variáveis de interesse: temperatura, precipitação e umidade do ar
            variables = ['temperature_2m', 'total_precipitation', 'dewpoint_temperature_2m']

            # Crie uma função para extrair os dados para cada imagem na coleção
            def extract_data(image):
                date = ee.Date(image.get('system:time_start')).format('YYYY-MM-DD')
                data = image.reduceRegion(
                    reducer=ee.Reducer.mean(),
                    geometry=self.location,
                    scale=1000,
                    maxPixels=1e9
                )
                
                # Crie um dicionário com a data e os valores de cada variável
                result = {
                    'date': date,
                    'temperature_2m': data.get('temperature_2m'),
                    'total_precipitation': data.get('total_precipitation'),
                    'dewpoint_temperature_2m': data.get('dewpoint_temperature_2m')
                }
                return ee.Feature(None, result)

            # Mapeie a função sobre a coleção de imagens e converta para uma lista de dicionários
            features = era5_image.map(extract_data)
            
            # Converta o resultado para um pandas DataFrame
            data_list = features.getInfo()['features']
            df = pd.DataFrame([feature['properties'] for feature in data_list])
            
            return df

        except ee.EEException as e:
            print(f"Erro ao coletar dados do Earth Engine: {e}")
            return None
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            return None

