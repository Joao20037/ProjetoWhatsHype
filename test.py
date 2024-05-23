from pygwalker.api.streamlit import StreamlitRenderer
import pandas as pd
import streamlit as st

# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Use Pygwalker In Streamlit",
    layout="wide"
)

# Add Title
st.title("Use Pygwalker In Streamlit")

# You should cache your pygwalker renderer, if you don't want your memory to explode
@st.cache_resource
def get_pyg_renderer() -> "StreamlitRenderer":
    df = pd.read_csv("C:\\Users\\T-GAMER\\Desktop\\ProjetoWhatsHype\\videos_musica.csv")
    
    # Filtrando os dados apenas para os top 10 vídeos
    top_10_videos = df['Video ID'].value_counts().nlargest(10).index
    df_top_10_videos = df[df['Video ID'].isin(top_10_videos)]
    df_top_10_videos['Data da Pesquisa'] = pd.to_datetime(df_top_10_videos['Data da Pesquisa'], format='%d/%m/%Y')
    df_top_10_videos = df_top_10_videos.sort_values(by='Data da Pesquisa')

    # Returning StreamlitRenderer with filtered data
    return StreamlitRenderer(df_top_10_videos, spec="./gw_config.json", spec_io_mode="rw")

renderer = get_pyg_renderer()

renderer.explorer()