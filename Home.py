import streamlit as st
from PIL import Image
import pandas as pd
import inflection
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

st.set_page_config(
    page_title="Home",
    page_icon="📉",
    layout="wide")


# =======================================================================================================================
# Funções
# =======================================================================================================================
def clean_code( df1 ):
    """ Esta função tem a responsabilidade de limpar o dataframe 

        Tipos de limpeza:
        1. Remoção das colunas do Dataframe que apresentam valores únicos e que não serão utilizadas
        2. Mudança do tipo da coluna de dados
        3. Categorização dos tipos de culinárias
        4. Remoção das informações duplicadas
        5. Preenchimento do nome dos países
        6. Remoção dos restaurantes com a informação de preço para dois zerado

        Input: Dataframe
        Output: Dataframe    
    """
    # 1.Removendo as colunas do Dataframe que não serão utilizadas
    df1 = df.drop(columns=['Switch to order menu'])
    
    # 2.Alteração do tipo de dados para String
    df1['Cuisines'] = df1['Cuisines'].astype( str )
    
    # 3.Mantendo somente um tipo de culinária por restaunte
    df1['Cuisines_categories'] = df1.loc[:, 'Cuisines'].astype(str).apply(lambda x: x.split(",")[0])
    
    # 4.Removendo as informações duplicadas
    df1 = df1.drop_duplicates().reset_index()
    
    # 5.Preenchimento do nome dos países
    df1['Country Name'] = df1['Country Code'].apply(country_name)
    
    # 6.Removendo os restaurantes com preço para dois = 0
    linhas_selecionadas = df1['Average Cost for two'] != 0
    df1 = df1.loc[linhas_selecionadas, :].copy()

    # 7.Convertendo a coluna 'Aggregate rating' para float
    #df1['Aggregate rating'] = df1['Aggregate rating'].astype(float)

    return df1


# Função que renomeia as colunas do DataFrame
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    

    return df


# Função que retorna os países de acordo com o código
def country_name(country_id):
    COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
    }

    return COUNTRIES[country_id]


# Função que cria o nome das cores
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
    }
def color_name(color_code):
    return COLORS[color_code]


def create_map(dataframe):
    df1 = rename_columns(df)
    
    f = folium.Figure(width=1920, height=1080)
    m = folium.Map(max_bounds=True).add_to(f)
    marker_cluster = MarkerCluster().add_to(m)

    for _, line in dataframe.iterrows():

        name = line["Restaurant Name"]
        price_for_two = line["Average Cost for two"]
        cuisine = line["Cuisines"]
        currency = line["Currency"]
        rating = line["Aggregate rating"]
        #color = f'{line["color_name"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price: {},00 ({}) para dois"
        html += "<br />Type: {}"
        html += "<br />Aggragate Rating: {}/5.0"
        html = html.format(name, price_for_two, currency, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["Latitude"], line["Longitude"]],
            popup=popup,
            #icon=folium.Icon(color=color, icon="home", prefix="fa"),
            icon=folium.Icon(icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(m, width=1024, height=768)

    return None


# ================================ Início da Estrutura Lógica do Código =================================================

# ================================
# Import dataset
# ================================
df = pd.read_csv( 'dataset/zomato.csv' )


# ===================================
# Renomeando as colunas do Dataframe
# ===================================
df1 = rename_columns(df)


# ================================
# Limpando os dados
# ================================
df1 = clean_code( df )


# =======================================================================================================================
# Barra Lateral no Streamlit
# =======================================================================================================================
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120 )

#st.sidebar.markdown( '# Fome Zero!' )
st.sidebar.markdown( '#### Conectando pessoas a restaurantes' )

country_options = st.sidebar.multiselect('Selecione os países dos quais deseja visualizar as informações',
                      ['India', 'Australia', 'Brazil', 'Canada', 'Indonesia', 'New Zeland', 'Philippines',
                      'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates',
                      'England', 'United States of America'],
                      default=['Brazil', 'Australia', 'United States of America', 'New Zeland', 'England', 'Qatar'])



# =======================================================================================================================
# Layout no Streamlit
# =======================================================================================================================
st.write( "# Fome Zero!")

st.markdown(
    """
    ##### Dashboard desenvolvido para acompanhar as métricas de crescimento dos restaurantes por país, cidades e tipos de culinárias.
    ##### Abaixo as marcas registradas em nossa plataforma até o momento:
    """
)

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        df_aux = df1['Restaurant ID'].count()

        st.metric(label='Restaurantes Cadastrados',
                  value=df_aux )

    with col2:
        df_aux = df1['Country Name'].nunique()

        st.metric(label='Países Cadastrados',
                  value=df_aux )

    with col3:
        df_aux = df1['City'].nunique()

        st.metric(label='Cidades Cadastradas',
                  value=df_aux )

    with col4:
        df_aux = df1['Votes'].sum()

        st.metric(label='Avaliações Feitas na Plataforma',
                  value=df_aux )

    with col5:
        df_aux = df1['Cuisines_categories'].nunique()

        st.metric(label='Tipos de Culinárias Oferecidas',
                  value=df_aux )

        
with st.container():
    map_df = df1.loc[df1['Country Name'].isin(country_options), :]
    create_map(map_df)
    


st.markdown(
    """
        ##### Ask for Help
    - Time de Data Science do Discord
        - @raquelcoelho
    """
)