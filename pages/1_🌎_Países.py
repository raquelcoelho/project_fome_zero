# Bibliotecas
import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px


st.set_page_config( page_title="Visão Países", page_icon="🌎", layout="centered" )

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

    return df1

    
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


# Função que renomeia as colunas do DataFrame
def rename_columns(dataframe):
    df1 = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new
    
    return df1


# Função que cria o Tipo de Categoria de Comida
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"


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


# Função que retorna a quantidade de restaurantes por país
def restaurants_by_country( df1 ):
    df_aux = df1.loc[:, ['Country Name', 'Restaurant ID']].groupby(['Country Name']).nunique().sort_values('Restaurant ID', ascending=False).reset_index()
    fig = px.bar(df_aux, x='Country Name', y='Restaurant ID', labels={'Country Name': 'País', 'Restaurant ID': 'Quantidade de Restaurantes'}, text_auto=True)
    fig.update_layout(title ='Quantidade de Restaurantes Registrados por País', title_x=0.3)

    return fig


# Função que retorna a quantidade de cidades registradas por país
def cities_by_country( df1 ):
    df_aux = (df1.loc[:, ['Country Name', 'City']].groupby(['Country Name'])
                                                  .nunique()
                                                  .sort_values('City', ascending=False)
                                                  .reset_index())
    fig = px.bar(df_aux, x='Country Name', y='City', labels={'Country Name': 'País', 'City': 'Quantidade de Cidades'}, text_auto=True)
    fig.update_layout(title ='Quantidade de Cidades Registradas por País', title_x=0.3)

    return fig


# Função que retorna a média de avaliações feitas por País
def reviews_by_country( df1 ):
    df_aux = (df1.loc[:, ['Country Name', 'Votes']].groupby('Country Name')['Votes'].mean().round().reset_index().sort_values('Votes', ascending=False))
    fig = px.bar(df_aux, x='Country Name', y='Votes', labels={'Country Name': 'País', 'Votes': 'Quantidade de Avaliações'}, text_auto=True)
    fig.update_layout(title ='Média de Avaliações feitas por País', title_x=0.2)

    return fig


# Função que retorna a média de um prato para duas pessoas por País
def plate_for_two_people( df1 ):
    df_aux = df1.loc[:, ['Country Name', 'Average Cost for two']].groupby('Country Name')['Average Cost for two'].mean().reset_index().round(2)
    fig = px.bar(df_aux, x='Country Name', y='Average Cost for two', labels={'Country Name': 'País', 'Average Cost for two': 'Preço de Prato para Duas Pessoas'}, text_auto=True)
    fig.update_layout(title ='Média de preço de prato para duas pessoas por País', title_x=0.1)

    return fig

# ================================ Início da Estrutura Lógica do Código =================================================

# ================================
# Import dataset
# ================================
df = pd.read_csv( 'dataset/zomato.csv' )

# ================================
# Limpando os dados
# ================================
df1 = clean_code( df )


# =======================================================================================================================
# Barra Lateral no Streamlit
# =======================================================================================================================
st.header("🌎 Visão Países")

image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120 )

#st.sidebar.markdown( '# Fome Zero' )
st.sidebar.markdown( '#### Conectando pessoas a restaurantes' )
st.sidebar.markdown( """___""" )


country_options = st.sidebar.multiselect('Selecione os países dos quais deseja visualizar as informações',
                      ['India', 'Australia', 'Brazil', 'Canada', 'Indonesia', 'New Zeland', 'Philippines',
                      'Qatar', 'Singapure', 'South Africa', 'Sri Lanka', 'Turkey', 'United Arab Emirates',
                      'England', 'United States of America'],
                      default=['Brazil', 'Australia', 'United States of America', 'New Zeland', 'England', 'Qatar'])

st.sidebar.markdown( """___""" )
st.sidebar.markdown( '##### Powered by Comunidade DS' )


# Filtro por país
linhas_selecionadas = df1['Country Name'].isin( country_options )
df1 = df1.loc[linhas_selecionadas, : ]

# =======================================================================================================================
# Layout no Streamlit
# =======================================================================================================================
with st.container():
    fig = restaurants_by_country( df1 )
    st.plotly_chart( fig, use_container_width=True)


with st.container():
    fig = cities_by_country( df1 )
    st.plotly_chart( fig, use_container_width=True)


with st.container():
    col1, col2 = st.columns(2)

    with col1:
        fig = reviews_by_country( df1 )
        st.plotly_chart( fig, use_container_width=True)

    with col2: 
        fig = plate_for_two_people( df1 )
        st.plotly_chart( fig, use_container_width=True)


















