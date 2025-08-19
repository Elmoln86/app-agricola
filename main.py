import streamlit as st
import ee

# --- Configurações da Página Streamlit ---
st.set_page_config(layout="wide", page_title="App Agrícola Inteligente")
st.title("Plataforma de Gestão Agrícola Inteligente")
st.markdown("Bem-vindo à sua plataforma integrada de análise e automação agrícola.")

# --- Autenticação e Inicialização da API do Google Earth Engine ---
# Este código foi corrigido para usar as credenciais do tipo "Authorized User"
# que você tem em seu secrets.toml (client_id, client_secret, refresh_token).
try:
    # A autenticação é feita com os dados do secrets.toml.
    credentials = ee.OAuth2Credentials(
        client_id=st.secrets["earthengine_credentials"]["client_id"],
        client_secret=st.secrets["earthengine_credentials"]["client_secret"],
        refresh_token=st.secrets["earthengine_credentials"]["refresh_token"],
        scopes=ee.oauth.SCOPES
    )
    ee.Initialize(credentials)
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

# --- Seu código de aplicativo original deve vir aqui abaixo ---
# Importe suas classes e inicie a lógica do aplicativo
# import earthengine-api
# ...
