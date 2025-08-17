import plotly.graph_objects as go
import pandas as pd

class DigitalTwin:
    def create_3d_visualization(self, data_points):
        """
        Cria uma visualização 3D da lavoura com pontos de dados.

        Args:
            data_points (DataFrame): DataFrame com colunas 'x', 'y', 'z' e 'cor' (ex: saúde da planta).
        """
        # Criar a figura 3D
        fig = go.Figure(data=[go.Scatter3d(
            x=data_points['x'],
            y=data_points['y'],
            z=data_points['z'],
            mode='markers',
            marker=dict(
                size=5,
                color=data_points['saude'],  # Mapear a cor com base em um valor (ex: NDVI)
                colorscale='Viridis',
                colorbar_title='Saúde da Planta',
                opacity=0.8
            )
        )])

        fig.update_layout(
            title='Gêmeo Digital da Lavoura de Café Conilon',
            scene=dict(
                xaxis_title='Posição X',
                yaxis_title='Posição Y',
                zaxis_title='Altura da Planta'
            )
        )
        return fig
