# Bibliotecas
import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px


st.set_page_config( page_title="Visão Cidades", page_icon="🏙️", layout="wide" )

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


# Função que retorna a quantidade de restaurantes por cidade
def restaurants_by_cities( df1 ):
    df_aux = (df1.loc[:, ['Country Name', 'City', 'Restaurant ID']].groupby(['City', 'Country Name'])
                                                                  .count()
                                                                  .reset_index()
                                                                  .sort_values('Restaurant ID', ascending=False)
                                                                  .head(10))
    fig = px.bar(df_aux, x='City', y='Restaurant ID', labels={'City': 'Cidade', 'Restaurant ID': 'Quantidade de Restaurantes', 'Country Name': 'País'}, text_auto=True, color='Country Name')
    fig.update_layout(title ='Top 10 Cidades com mais Restaurantes na Base de Dados', title_x=0.2)

    return fig


# Função que retorna as cidades com restaurantes com média de avaliação acima de 4
def restaurants_highest_rating( df1 ):
    df_aux = (df1.loc[:, ['City', 'Country Name', 'Restaurant ID']].groupby(['City', 'Country Name'])
                                                                   .count()
                                                                   .reset_index()
                                                                   .sort_values('Restaurant ID', ascending=False)
                                                                   .head(7))
    fig = px.bar(df_aux, x='City', y='Restaurant ID', labels={'City': 'Cidade', 'Restaurant ID': 'Quantidade de Restaurantes', 'Country Name': 'País'}, text_auto=True, color='Country Name')
    fig.update_layout(title ='Top 7 Cidades com Restaurantes com média de avaliação acima de 4', title_x=0)

    return fig


# Função que retorna as cidades com restaurantes com média de avaliação abaixo de 2.5
def restaurants_lowest_rating( df1 ):
    linhas_selecionadas = df1['Aggregate rating'] <= 2.5
    df_aux = (df1.loc[linhas_selecionadas, ['City', 'Country Name', 'Restaurant ID']].groupby(['City', 'Country Name'])['Restaurant ID']
                                                                                     .count()
                                                                                     .reset_index()
                                                                                     .sort_values('Restaurant ID', ascending=False)
                                                                                     .head(7))
    fig = px.bar(df_aux, x='City', y='Restaurant ID', labels={'City': 'Cidade', 'Restaurant ID': 'Quantidade de Restaurantes', 'Country Name': 'País'}, text_auto=True, color='Country Name')
    fig.update_layout(title ='Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5', title_x=0)

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
st.header("🏙️ Visão Cidades")

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
    fig = restaurants_by_cities( df1 )
    st.plotly_chart( fig, use_container_width=True)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        fig = restaurants_highest_rating( df1 )
        st.plotly_chart( fig, use_container_width=True)

    with col2:
        fig = restaurants_lowest_rating( df1 )
        st.plotly_chart( fig, use_container_width=True)

with st.container():
    df_aux = df1.loc[:, ['City', 'Cuisines_categories', 'Country Name']].groupby(['City', 'Country Name']).nunique().reset_index().sort_values('Cuisines_categories', ascending=False).head(10)
    fig = px.bar(df_aux, x='City', y='Cuisines_categories', labels={'City': 'Cidade', 'Cuisines_categories': 'Quantidade de Tipos Culinários Únicos', 'Country Name': 'País'}, text_auto=True, color='Country Name')
    fig.update_layout(title ='Top 10 Cidades com mais restaurantes com tipos culinários distintos', title_x=0.1)
    st.plotly_chart( fig, use_container_width=True)

    



















