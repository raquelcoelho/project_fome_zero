# Bibliotecas
import pandas as pd
import streamlit as st
from PIL import Image
import plotly.express as px
import inflection


st.set_page_config( page_title="Visão Culinárias", page_icon="🍽️", layout="wide" )

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


# Função que retorna os 10 melhores tipos de culinárias
def top_best_cuisines( df1 ):
    df_aux = (df1.loc[:, ['restaurant_id', 'cuisines_categories', 'aggregate_rating']].groupby('cuisines_categories')['aggregate_rating']
                                                                  .mean()
                                                                  .round(2)
                                                                  .reset_index()
                                                                  .sort_values('aggregate_rating', ascending=False)
                                                                  .head(10))
    
    fig = px.bar(df_aux, x='cuisines_categories', y='aggregate_rating', labels={'cuisines_categories': 'Tipo de Culinária', 'aggregate_rating': 'Avaliação Média'}, text_auto=True)
    fig.update_layout(title ='Top 10 Melhores Tipos de Culinárias', title_x=0.2)

    return fig


# Função que retorna os 10 piores tipos de culinárias
def top_worst_cuisines( df1 ):
    df_aux = (df1.loc[:, ['restaurant_id', 'cuisines_categories', 'aggregate_rating']].groupby('cuisines_categories')['aggregate_rating']
                                                                  .mean()
                                                                  .round(2)
                                                                  .reset_index()
                                                                  .sort_values('aggregate_rating', ascending=True)
                                                                  .head(10))
    
    fig = px.bar(df_aux, x='cuisines_categories', y='aggregate_rating', labels={'cuisines_categories': 'Tipo de Culinária', 'aggregate_rating': 'Avaliação Média'}, text_auto=True)
    fig.update_layout(title ='Top 10 Piores Tipos de Culinárias', title_x=0.2)

    return fig
    

# ================================ Início da Estrutura Lógica do Código =================================================

# ================================
# Import dataset
# ================================
df = pd.read_csv( 'dataset/zomato.csv' )

# ===================================
# Renomeando as colunas do Dataframe
# ===================================
df1 = rename_columns(df)
df_rest = rename_columns(df)


# ================================
# Limpando os dados
# ================================
df1 = clean_code( df )
df_rest = clean_code( df )


# =======================================================================================================================
# Barra Lateral no Streamlit
# =======================================================================================================================
st.header('🍽️ Visão Tipos de Culinárias')

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


# Filtro da quantidade de restaurantes
num_rest = st.sidebar.slider('Selecione a quantidade de restaurantes que deseja visualizar', value=10, min_value=0, max_value=50)


# Filtro por tipo de culinária
type_cuisines = list(df1['Cuisines_categories'].unique())
cuisines_options = st.sidebar.multiselect('Selecione os tipos de culinárias:', type_cuisines,
                                         default=['American', 'Italian', 'Arabian', 'Japanese', 'Brazilian'])


# Filtro por País e tipo de culinária
linhas_selecionadas = (df1['Country Name'].isin( country_options )) | (df1['Cuisines_categories'].isin( cuisines_options ))
df1 = df1.loc[linhas_selecionadas, : ]


# =======================================================================================================================
# Layout no Streamlit
# =======================================================================================================================
with st.container():
    st.markdown('### Melhores Restaurantes dos Principais Tipos Culinários')
    df1 = rename_columns(df1)
    df_rest = rename_columns(df_rest)
    cols = ['aggregate_rating', 'restaurant_id', 'restaurant_name', 'average_cost_for_two', 'currency', 'votes', 'country_name', 'city']
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        linhas_selecionadas = df_rest['cuisines_categories'] == 'Italian'
        df_aux = df_rest.loc[linhas_selecionadas, cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).reset_index().head()
        italian_rest = df_aux

        st.metric(label=f'Italian: {italian_rest.restaurant_name[0]}', 
                  value=f'{italian_rest.aggregate_rating[0]}/5.0',
                  help=f"""
                  País: {italian_rest.country_name[0]} \n
                  Cidade: {italian_rest.city[0]} \n
                  Preço para duas pessoas: {italian_rest.currency[0]}{italian_rest.average_cost_for_two[0]} 
                  """
                )

    with col2:
        linhas_selecionadas = df_rest['cuisines_categories'] == 'American'
        df_aux = df_rest.loc[linhas_selecionadas, cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).reset_index().head()
        american_rest = df_aux

        st.metric(label=f'American: {american_rest.restaurant_name[0]}', 
                  value=f'{american_rest.aggregate_rating[0]}/5.0',
                  help=f"""
                  País: {american_rest.country_name[0]} \n
                  Cidade: {american_rest.city[0]} \n
                  Preço para duas pessoas: {american_rest.currency[0]}{american_rest.average_cost_for_two[0]} 
                  """
                )

    with col3:
        linhas_selecionadas = df_rest['cuisines_categories'] == 'Arabian'
        df_aux = df_rest.loc[linhas_selecionadas, cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).reset_index().head()
        arabian_rest = df_aux

        st.metric(label=f'Arabian: {arabian_rest.restaurant_name[0]}', 
                  value=f'{arabian_rest.aggregate_rating[0]}/5.0',
                  help=f"""
                  País: {arabian_rest.country_name[0]} \n
                  Cidade: {arabian_rest.city[0]} \n
                  Preço para duas pessoas: {arabian_rest.currency[0]}{arabian_rest.average_cost_for_two[0]} 
                  """
                )

    with col4:
        linhas_selecionadas = df_rest['cuisines_categories'] == 'Japanese'
        df_aux = df_rest.loc[linhas_selecionadas, cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).reset_index().head()
        japanese_rest = df_aux

        st.metric(label=f'Japanese: {japanese_rest.restaurant_name[0]}', 
                  value=f'{japanese_rest.aggregate_rating[0]}/5.0',
                  help=f"""
                  País: {japanese_rest.country_name[0]} \n
                  Cidade: {japanese_rest.city[0]} \n
                  Preço para duas pessoas: {japanese_rest.currency[0]}{japanese_rest.average_cost_for_two[0]} 
                  """
                )

    with col5:
        linhas_selecionadas = df_rest['cuisines_categories'] == 'Brazilian'
        df_aux = df_rest.loc[linhas_selecionadas, cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).reset_index().head()
        brazilian_rest = df_aux

        st.metric(label=f'Brazilian: {brazilian_rest.restaurant_name[0]}', 
                  value=f'{brazilian_rest.aggregate_rating[0]}/5.0',
                  help=f"""
                  País: {brazilian_rest.country_name[0]} \n
                  Cidade: {brazilian_rest.city[0]} \n
                  Preço para duas pessoas: {brazilian_rest.currency[0]}{brazilian_rest.average_cost_for_two[0]} 
                  """
                )

with st.container():
    st.markdown('### Top 10 Restaurantes')
    
    cols = ['restaurant_id', 'restaurant_name', 'country_name', 'city', 'cuisines_categories', 'average_cost_for_two', 'aggregate_rating', 'votes']
    top_rest = df1.loc[: , cols].sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).head(10)
    st.dataframe(top_rest, hide_index=True
   # st.dataframe(top_rest, hide_index=True,
   #              column_config={
   #                  "restaurant_id": st.column_config.NumberColumn( format="%.0f" ),
   #                  "average_cost_for_two": st.column_config.NumberColumn( format="%.2f" ),
   #                  "votes": st.column_config.NumberColumn( format="%.0f" )}
                )

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        fig = top_best_cuisines( df1 )
        st.plotly_chart( fig, use_container_width=True)

    with col2:
        fig = top_worst_cuisines( df1 )
        st.plotly_chart( fig, use_container_width=True)
        



    
        

    



















