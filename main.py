import streamlit as st
import ee

# --- Configurações da Página Streamlit ---
st.set_page_config(page_title="Teste de Autenticação do Earth Engine")
st.title("Teste de Autenticação do Google Earth Engine")
st.markdown("Este aplicativo foi criado para testar se a autenticação com o Earth Engine está funcionando corretamente.")

# --- Autenticação e Inicialização da API do Google Earth Engine ---
# O método ee.Initialize() tentará se autenticar usando as credenciais do Streamlit Cloud.
# Se a autenticação falhar, uma exceção será capturada e uma mensagem de erro será exibida.
try:
    ee.Initialize()
    st.success("🎉 A autenticação com o Google Earth Engine foi bem-sucedida! 🎉")
    st.write("Isso significa que suas credenciais estão corretas e sua conta está aprovada.")

    # Exemplo de teste simples para confirmar a conexão
    st.header("Teste de Conexão com a API")
    try:
        # Acessa uma geometria de ponto e a exibe.
        # Se esta linha for executada, a conexão está funcionando.
        location = ee.Geometry.Point([-47.9382, -15.7801])
        st.write("Conexão com o Earth Engine estabelecida com sucesso!")
        st.write(f"Geometria de teste: {location.getInfo()}")
    except ee.EEException as e:
        st.error(f"Erro ao executar o teste da API. O problema ainda pode ser na sua conta. Erro: {e}")

except Exception as e:
    st.error("❌ Erro ao inicializar o Google Earth Engine. ❌")
    st.write("Ocorreu um problema com a autenticação.")
    st.write("Por favor, verifique os seguintes pontos:")
    st.markdown("- Suas credenciais no arquivo `secrets.toml` estão corretas.")
    st.markdown("- Sua conta Google foi aprovada para usar o Earth Engine.")
    st.markdown(f"**Detalhes do erro:** {e}")

