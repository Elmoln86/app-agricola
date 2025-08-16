import ee
import geemap

class SatelliteCollector:
    def __init__(self):
        try:
            # Tenta inicializar a API do GEE
            ee.Initialize()
        except Exception:
            # Autentica o usuário se a API não estiver inicializada
            ee.Authenticate()
            ee.Initialize()
        
    def get_ndvi(self, lat, lon, start_date, end_date):
        """
        Coleta dados de NDVI (Índice de Vegetação da Diferença Normalizada)
        da imagem do satélite Sentinel-2 para uma área e período específicos.
        """
        # Ponto de interesse
        point = ee.Geometry.Point(lon, lat)

        # Filtra a coleção de imagens Sentinel-2 por data e localização
        sentinel_collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')\
            .filterDate(start_date, end_date)\
            .filterBounds(point)\
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) # Filtra imagens com poucas nuvens

        # Mapeia a coleção para calcular o NDVI para cada imagem
        def calculate_ndvi(image):
            # As bandas são B8 (NIR) e B4 (Red) para o Sentinel-2
            ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
            return image.addBands(ndvi)

        # Aplica a função e obtém a imagem com o maior NDVI no período
        ndvi_collection = sentinel_collection.map(calculate_ndvi)
        median_ndvi = ndvi_collection.median().select('NDVI')

        # Obtém o valor do NDVI no ponto de interesse
        ndvi_value = median_ndvi.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=10 # Resolução de 10 metros
        ).get('NDVI').getInfo()

        return ndvi_value

# Exemplo de uso
# sat_collector = SatelliteCollector()
# ndvi_value = sat_collector.get_ndvi(-20.27, -40.30, '2025-01-01', '2025-01-31')
# print(f"Valor médio de NDVI no período: {ndvi_value}")
