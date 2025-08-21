import streamlit as st
import ee

st.set_page_config(
    page_title="Plataforma de Gestão Agrícola Inteligente",
    layout="wide"
)

# Título da aplicação
st.title("Plataforma de Gestão Agrícola Inteligente")
st.markdown("Bem-vindo à sua plataforma integrada de análise e automação agrícola.")

# Mensagem de status
status_message = st.empty()

# Corrigido: Usando st.secrets para acessar as credenciais do secrets.toml
try:
    # Acessa os segredos do Streamlit Cloud
    ee_client_email = st.secrets["earthengine"]["earthengine_client_email"]
    ee_private_key = st.secrets["earthengine"]["earthengine_private_key"]
    
    # Exibe uma mensagem de status para o usuário
    status_message.info("Conectando ao Google Earth Engine...")
    
    # Inicializa a API do Earth Engine com as credenciais da conta de serviço
    # A correção está aqui: a chave privada é passada como uma string diretamente.
    credentials = ee.ServiceAccountCredentials(ee_client_email, ee_private_key)
    ee.Initialize(credentials)
    
    # Se a inicialização for bem-sucedida, exibe uma mensagem de sucesso
    status_message.success("Conexão com o Google Earth Engine bem-sucedida!")

    # Exemplo de código GEE para mostrar que a autenticação funcionou
    # Apenas como um teste simples
    # Ponto de exemplo (Bragança Paulista)
    point = ee.Geometry.Point([-46.5413, -22.9545])
    
    # Imagem Landsat
    landsat_image = ee.Image('LANDSAT/LC08/C01/T1_SR/LC08_219076_20170118')
    
    # Recorta a imagem
    clipped_image = landsat_image.clip(point.buffer(10000))
    
    # Exibe o mapa na interface
    st.write("Exemplo de Imagem Landsat:")
    # Acha o ponto central
    center = clipped_image.geometry().centroid().getInfo()['coordinates']
    
    # Cria a URL do mapa
    landsat_viz = {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000, 'gamma': 1.4}
    map_id = landsat_image.getMapId(landsat_viz)
    
    st.image(f"https://earthengine.googleapis.com/v1alpha/projects/{ee.data._get_project_name()}/maps/{map_id['mapid']}/tiles/{{z}}/{{x}}/{{y}}",
             caption="Imagem Landsat (visualização RGB)",
             use_column_width=True)

    st.write("A sua autenticação funcionou, agora você pode continuar com o desenvolvimento!")

except Exception as e:
    # Se ocorrer qualquer erro, exibe a mensagem de erro completa
    st.error(f"Erro ao inicializar o Google Earth Engine: {e}")
    st.warning("Verifique se as credenciais no painel de segredos do Streamlit Cloud estão corretas e se sua conta tem as permissões de acesso ao Earth Engine.")
    st.info("Para mais informações sobre o erro, verifique os logs de implantação no Streamlit Cloud.")
