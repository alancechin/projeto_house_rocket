# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 10:57:13 2022

@author: alanc
"""

## Libraries ###-------------------------------------------------------------------

import geopandas
import pandas as pd
import numpy as np
import streamlit as st 
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px
from datetime import datetime


## Functions ###-------------------------------------------------------------------------------------

# Configurar formas de visualização para seguir o tamanho da página
st.set_page_config( layout= 'wide' )


## Para poupar tempo em extrair informação da memória cache e não do disco
@st.cache( allow_output_mutation = True )

## Função para carregar base de dados de imóveis de arquivo em formato .csv
def get_data( path ):
    
    data = pd.read_csv( path )
    
    return data 

# Função para extrair informações/dados de API sobre coordenadas (LAT, LONG) de regiões representadas pelo zipcode da cidade trabalhada
@st.cache( allow_output_mutation=True )
def get_geofile( url ):
    
    geofile = geopandas.read_file( url )

    return geofile


def data_cleaning(df):
    
    ## DATA CLEANING ------------------------------------------------------
    
    ## Outliers -----------------------------------------------------------
    
    df.loc[df['bedrooms'] == 33, 'bedrooms' ] = 3
    
    ## Tratamento e criação de features -----------------------------------
    
    # Tratar coluna date para ficar do tipo datetime
    df['date'] = pd.to_datetime(df['date'], format = ('%Y-%m-%d'))
    
    # Coluna para data com formato em Dia/Mês/Ano
    df['date_str'] = df['date'].dt.strftime('%d-%m-%Y')
    
    # Criar colunas separadas para mês e ano de venda do imóvel
    df['month'] = df['date'].dt.month 
    df['year'] = df['date'].dt.year

    # Criar coluna para estações do ano - Verão, Inverno, Primavera, Outono.
    
    #Verão: de junho a agosto.
    #Outono: de setembro a novembro.
    #Inverno: de dezembro a fevereiro.
    #Primavera: de março a maio.#
    
    ver_lt = [6,7,8]
    out_lt = [9,10,11]
    inv_lt = [12,1,2]
    pri_lt = [3,4,5]
    
    
    df.loc[df['month'].isin(ver_lt), 'seasons'] = 'Verão'
    df.loc[df['month'].isin(out_lt), 'seasons'] = 'Outono'
    df.loc[df['month'].isin(inv_lt), 'seasons'] = 'Inverno'
    df.loc[df['month'].isin(pri_lt), 'seasons'] = 'Primavera'
    
    # Criar uma coluna nova com unidade de medida de área m2 para o tamanho do imóvel
    df['m2_living'] = df['sqft_living']/ 10.764
    df['m2_lot'] = df['sqft_lot']/ 10.764
    df['m2_above'] = df['sqft_above']/ 10.764
    
    
    #- Criar coluna extra que seria tamanho área externa -> sqft_outside = sqft_lot - (sqft_above/floors)
    df['m2_outside'] = df['m2_lot'] - (df['m2_above']/df['floors'])
    
    # Criar coluna preço imóvel / área construída (m2_living) 
    df['price_per_m2_living'] = df['price'] / df['m2_living']
    
    # Criar coluna preço imóvel / área construída + área externa
    df['price_per_m2_living_outside'] = df['price'] / (df['m2_living'] + df['m2_outside'])
    
    # Criar coluna age
    df['age'] = datetime.now().year - df['yr_built']
    
    # Criar coluna is_renovated
    df['is_renovated'] = df['yr_renovated'].apply(lambda x: 'Yes' if x != 0 else 'No')
    
    # Troca de valores waterfront: (0) -> No (1) -> Yes
    df['waterfront'].replace({1:'Yes',0:'No'}, inplace = True)
    
    df = df[['id','zipcode', 'date', 'date_str', 'month', 'year', 'yr_built', 'age', 'yr_renovated', 
             'is_renovated', 'bathrooms','bedrooms','condition','floors','grade', 'lat','long',
             'm2_living', 'm2_outside', 'price', 'price_per_m2_living', 'price_per_m2_living_outside',
             'seasons', 'view','waterfront']]
    
    return df



def table_metrics(df):
    
    
    ## 1.1 - Dataframes com métricas por região(zipcode)  
    
    # Número de imóveis distintos por região
    n_imoveis = df[['zipcode','id']].groupby(['zipcode']).nunique().reset_index()
    # Média de preço dos imóveis por região
    media_price = df[['zipcode','price']].groupby(['zipcode']).mean().reset_index()
    # Média da área contruída imóveis (m2) por região
    media_m2_living = df[['zipcode','m2_living']].groupby(['zipcode']).mean().reset_index()
    # Preço por área construída (m2) médio por região
    media_price_per_m2_b = df[['zipcode','price_per_m2_living']].groupby(['zipcode']).mean().reset_index()
    # Área externa média dos imóveis (m2) por região
    media_m2_outside = df[['zipcode','m2_outside']].groupby(['zipcode']).mean().reset_index()
    # Preço por área construída + área externa (m2) médio por região
    media_price_per_m2_f = df[['zipcode','price_per_m2_living_outside']].groupby(['zipcode']).mean().reset_index()
    
    
    # Merge tables - Unir todas as tabelas sobre zipcode
    m = n_imoveis.merge(media_price, on = 'zipcode', how = 'inner').merge(media_price_per_m2_b, on = 'zipcode', how = 'inner').merge(media_price_per_m2_f, on = 'zipcode', how = 'inner').merge( media_m2_living , on = 'zipcode', how = 'inner').merge( media_m2_outside , on = 'zipcode', how = 'inner')
    
    # Dar nome colunas
    m.columns = ['Código Postal', 'Quantidade','Preço','Preço / m2 construído', 
                 'Preço / m2 construído + área externa ', 'm2 construído', 'm2 externo']
    
    
    ## 1.3 - Dataframe com estatística descritiva dos atributos da base de dados 
    
    df_var_ed = df[[ 'year', 'age', 'yr_renovated', 'bathrooms','bedrooms','condition','floors','grade', 
                    'm2_living', 'm2_outside', 'price', 'price_per_m2_living', 'price_per_m2_living_outside']]
    
    media_ed = pd.DataFrame( df_var_ed.apply(np.mean, axis = 0) )
    mediana_ed = pd.DataFrame( df_var_ed.apply(np.median, axis = 0) )
    desv_pad_ed = pd.DataFrame( df_var_ed.apply(np.std, axis = 0) )
    max_ed = pd.DataFrame( df_var_ed.apply(np.max, axis = 0) )
    min_ed = pd.DataFrame( df_var_ed.apply(np.min, axis = 0) )
    
    
    # Juntar Medidas estatísticas de atributos em tabelas diferentes
    
    ed = pd.concat([media_ed, mediana_ed, desv_pad_ed, max_ed, min_ed], axis = 1).reset_index()
    
    # Dar nome colunas
    
    ed.columns = ['Atributos','Média','Mediana','Desvio Padrão','Máximo','Mínimo']
    
    return m, ed



def maps(df, geofile):
    
    
    # 2. Mapas
    
    
    # 2.1 Densidade de Portfolio - Distribuição/Quantidade de imóveis por região


    #data_map = df.sample( 10 ) # Pegar apenas 10 amostras de imóveis
    
    # Mapa Base - Folium - é apenas o mapa sem pontos
    density_map = folium.Map( location=[df['lat'].mean(), 
                                        df['long'].mean() ], 
                                        default_zoom_start=15 )
    
    
    # Instanciando objeto para inserir os dados de imóveis no mapa, os pontos
    marker_cluster = MarkerCluster().add_to( density_map )
    
    # Inserção dos pontos imóveis no mapa transformando dataframe com dados em iterativo para usar o for com estruturas dataframe
    # row = linha -> imóveis/amostra/observação distinta
    # popup = descrição ao passar o mouse sobre os pontos
    for name, row in df.iterrows():
        
        folium.Marker( [row['lat'], row['long'] ], popup='''Vendido por ${0} em: {1}. Características: {2} m2 de área construída, 
                                                          {3} quartos,{4} banheiros, ano construção: {5}'''.format( row['price'],
                                                                                                                     row['date_str'],
                                                                                                                     row['m2_living'],
                                                                                                                     row['bedrooms'],
                                                                                                                     row['bathrooms'],
                                                                                                                     row['yr_built'] ) ).add_to( marker_cluster )
    
    

    
    
    # 2.3 Region Price per m2 built Map - 
    
    data_map = df[['price_per_m2_living','zipcode']].groupby( ['zipcode'] ).mean().reset_index() 
    
    data_map.columns = ['ZIP', 'PRICE']
        
    
    # Filtrar do arquivo com as coordenadas de regiões totais apenas as regiões de amostra que peguei para analisar preço médio no dataset 
    # para depois não acabar ficando regiões sem dado de preço médio
    geofile = geofile[geofile['ZIP'].isin( data_map['ZIP'].tolist() )]
    
    # Mapa Base - Folium - é apenas o mapa sem pontos
    region_price_liv_map = folium.Map( location= [df['lat'].mean(), df['long'].mean() ], default_zoom_start=15 )
    
    
    folium.Choropleth( data = data_map, geo_data = geofile, columns=['ZIP', 'PRICE'],
                                 key_on='feature.properties.ZIP', fill_color='YlOrRd',
                                 fill_opacity = 0.7, line_opacity = 0.2,
                                 legend_name='PREÇO/ÁREA CONSTRUÍDA MÉDIO' ).add_to(region_price_liv_map)
    

    

    return density_map, region_price_liv_map 


def compra_house(x):
    if (x['price_per_m2_living'] < x['target_buy']) & (x['condition'] >= 3) & (x['age'] >= 50):
        
        if (x['is_renovated'] == 1):
            return 'Compra'
        else:
            return 'Não Compra'
        
    elif (x['price_per_m2_living'] < x['target_buy']) & (x['condition'] >= 3) & (x['age'] < 50):
        return 'Compra'
    
    else:
        return 'Não Compra'



def venda_house(x):
         
    if (x['price_per_m2_living'] >= x['median_venda']) & (x['grade'] > x['mean_grade_per_zip']):
        return x['price']* 1.1
    elif (x['price_per_m2_living'] >= x['median_venda']):
        return x['price']* 1.05
    elif (x['price_per_m2_living'] < x['median_venda']) & (x['grade'] > x['mean_grade_per_zip']):
        return x['price']* 1.2
    elif (x['price_per_m2_living'] < x['median_venda']):
        return x['price']* 1.15
    

def aplic(x):
    
    cor = 'blue' if x == 'Compra' else 'black' 
    return f'color: {cor}'



### -----------------------------------------------------------------------------------


# Função que ao rodar o script interpretador procura essa função para começar por aqui
# Inteligência do Código 
# ETL
if __name__ == '__main__':

#================================================================================
## Extract ###-------------------------------------------------------------------
#================================================================================    
    
    ## Extrair base de imóveis
    path = 'kc_house_data.csv'
    df = get_data(path)
        
    ## Extrair infomações das coordenadas das regiões por CEP de Seattle - Virá um dicionário com lista aninhada de coordenadas das regiões
    
    ## Servidor na nuvem com dados de localização utilizando endereço eletrônico
    #url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
    
    # Arquivo baixado localmente com dados de localização
    url = 'Zip_Codes.geojson'
    
    # Leitura dos dados 
    geofile = get_geofile( url )

#######################################################################################   
    
    ## Criação de Abas no layout da páginas
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Sobre", "📈 Visão Geral", "💡 Insights", "💎 Recomendações de Investimento"]) 

    ## FUNC 1
    df_clean = data_cleaning(df)
    
    
 
    
    with tab1:
    
        
        st.markdown('''A House Rocket é uma empresa que realiza investimentos no mercado imobiliário. Tem por 
                     modelo de negócio realizar estudos sobre regiões onde deseja realizar operações e ter assertividade 
                     no portfólio de ativos imobiliários. Sua estratégia é comprar bons imóveis com lacuna de 
                     oportunidade de crescimento no preço para vender e obter lucros.
                     O desafio no momento é iniciar operações no estado de Washington - EUA, na cidade de Seattle. ''')
        
        col1, col2, col3, col4, col5 = st.columns((1, 0.2, 1, 0.2, 1))
        
        col1.subheader("📈Visão Geral")
        col1.markdown(''' Para esse novo desafio, utilizou-se uma base de dados para análise que consiste em 21.613 vendas
                      de imóveis realizadas entre as datas de 02/05/2014 à 27/05/2015 na cidade de Seattle - EUA. Essa base
                      de dados conta com informações de venda de 21.436 imóveis distintos. ''')
                      
        col1.markdown(''' Nessa aba você poderá conferir, se desejar filtrando por Código Postal, por meio de tabelas, 
                      mapas e gráficos um pouco mais sobre as características desses imóveis. ''')
        
        col3.subheader("💡 Insights")
        col3.markdown('''Por meio de pesquisas com profissionais e economistas que trabalham com o mercado imobiliário 
                      de Seattle - EUA, levantaram-se conhecimentos empíricos sobre fatores e características que 
                      impactam os ativos imobiliários da região. ''')
        
        col3.markdown(''' Nessa aba o objetivo é analisar com dados a validade de algumas hipóteses levantadas por 
                      especialistas do mercado.''')
        
        
        col5.subheader("💎 Recomendações de Investimento")
        col5.markdown('''Alinhado com a estratégia da empresa, nessa aba você poderá conferir alguns imóveis que foram 
                      apontados como potenciais para compra e o preço estimado. Além disso, foram projetados os valores
                      de venda desses imóveis indicados para compra, visando assim, projetar os retornos dos futuros
                      investimentos realizados.''')
        
        
    
    with tab2:
        
        # Filtro 
        f_zip_code = st.multiselect('Selecione Código Postal:', options = df['zipcode'].sort_values().unique().tolist() )
        
        # Filtragem dos dados por zipcode 
        
        if (f_zip_code != []): 
            df_raw_f = df.loc[ df['zipcode'].isin(f_zip_code) , :].reset_index(drop = True) 
            df_clean_f = df_clean.loc[df_clean['zipcode'].isin(f_zip_code) , : ].reset_index(drop = True)
       
        else:
            df_raw_f = df.copy() ## Se tiver tudo vazio, não selecionar nada para não precisar ficar sem tabela, mostra ela completa
            df_clean_f = df_clean.copy()
        
        
        ## Abrir em 3 visualizações da Visão Geral
        tab1_viz = st.radio("Visualizar com:", ('Tabelas', 'Mapas', 'Gráficos'), horizontal = True)
        
        
        ### Tabelas ----------------------------------------------------------
        if tab1_viz == 'Tabelas':
            
            ### DADOS BRUTOS
            see_data1 = st.expander('Você pode clicar aqui para ver os dados brutos 👉')
            with see_data1:
                    
                
                f_colunas = st.multiselect('Selecione Atributos:', options = df_raw_f.columns.sort_values().tolist() )
                
                
                if (f_colunas != []): 
                    
                    st.dataframe( data= df_raw_f.loc[ : , f_colunas].reset_index(drop = True) )
               
                else:
                    st.dataframe( data= df_raw_f )## Se tiver tudo vazio, não selecionar nada para não precisar ficar sem tabela, mostra ela completa
                       
            ### DADOS TRATADOS
            see_data2 = st.expander('Você pode clicar aqui para ver os dados tratados 👉')
            with see_data2:  
    
                f_colunas = st.multiselect('Selecione Atributos:', options = df_clean_f.columns.sort_values().tolist() )
    
    
                if (f_colunas != []): 
                    
                    st.dataframe( data = df_clean_f.loc[ : , f_colunas].reset_index(drop = True) )
       
                else:
                    st.dataframe( data= df_clean_f ) ## Se tiver tudo vazio, não selecionar nada para não precisar ficar sem tabela, mostra ela completa
                    
            
            ## FUNC 2
            ### 1.TABLE ANALYSIS
            
            m_per_zip, ed = table_metrics(df_clean_f)
    
            
            # Para as tabelas ficarem lado a lado
            c1, c2, c3 = st.columns( (1, 0.2, 0.7) ) 
        
            ## 1.1 - Tabela com métricas por Região (Código Postal)
            c1.header('Imóveis por Região')   
            
            c1.markdown('Análise da quantidade, média de preços e área de imóveis por região (código postal)') 
            
            # Filtro de colunas Métricas por região
            f_colu = c1.multiselect('Selecione Colunas:', options = m_per_zip.columns.sort_values().tolist() )
            
            
            ## Dados Selecionados e apresentados
            if (f_colu != []):
                
                c1.write( m_per_zip.loc[:, f_colu ] )
                
            else:
                
                c1.write( m_per_zip )
            
            ## 1.2 - Tabela com estatística descritiva dos atributos
            c3.header('Estatística Descritiva')
            
            # Filtro de colunas Estatística Descritiva dos atributos
            f_colu = c3.multiselect('Selecione Colunas:', options = ed.columns.sort_values().tolist() )
            
            
            ## Dados Selecionados e apresentados
            if (f_colu != []):
                
                c3.write( ed.loc[:, f_colu ] )
                
            else:
                
                c3.write( ed )
            
            
            
        ### Tabelas ----------------------------------------------------------
        if tab1_viz == 'Mapas':
    
            ## FUNC 3
            density, price_int = maps(df_clean_f, geofile)
        
            
            c4, c5 = st.columns( ( 1, 1) )
        
            with c4:
        
        
                st.header('Densidade de imóveis')
                st.markdown("Análise da distribuição dos imóveis vendidos.")
                folium_static( density )
        
            with c5:
                
                st.header( 'Preço por área construída' )
                st.markdown("Análise do preço por área interna habitável (em metros quadrados) médio por região.")
                folium_static( price_int )    
                
                

        ### Gráficos ----------------------------------------------------------
        if tab1_viz == 'Gráficos':
        
            # 3. Gráficos 
            
            ### FILTROS ------------------------------------------------------------------------------
            
            st.subheader("Filtros:")
            
            c8, c9, c10, c11, c12  = st.columns( ( 1, 0.1 , 1, 0.1 , 1) )
            
            # 1.Filtro Ano de Construção # min. 1900 e máx. 2015 
        
        
            max_built = int(df_clean_f["yr_built"].min())
            min_built = int(df_clean_f["yr_built"].max())
        
        
        
            f_ano_construcao = c8.slider('Ano de construção:', min_value = min_built, 
                                                                   max_value = max_built,
                                                                   value = ( min_built , max_built ) )
        
            
            # 2. Filtro por data de venda
            
            
            f_disp = c10.slider("Período Venda: ", min_value = df_clean_f["date"].min() , 
                                                          max_value = df_clean_f["date"].max(),
                                                          value= (datetime(2014,5,2), datetime(2015,5,27)),
                                                          format="DD/MM/YY")
            
            
            # 3. Filtro por preço
            
            max_price = int(df_clean_f["price"].min())
            min_price = int(df_clean_f["price"].max())
            
            f_price = c12.slider('Preço:', min_value = min_price, max_value = max_price,
                                                               value = ( min_price , max_price ) )
            
            c13, c14, c15, c16, c17  = st.columns( ( 1, 0.1 , 1, 0.1 , 1) )
            
            # 4. Filtro por condição
            
            max_cond = int(df_clean_f["condition"].min())
            min_cond = int(df_clean_f["condition"].max())
            
            f_condition = c13.slider('Condição:', min_value = min_cond, max_value = max_cond,
                                                               value = ( min_cond , max_cond ) )
            
            # 5. Filtro por grade
            
            min_grade = int(df_clean_f["grade"].min())
            max_grade = int(df_clean_f["grade"].max())
            
            f_grade = c15.slider('Avaliação Construção:', min_value = min_grade, max_value = max_grade,
                                                               value = ( min_grade , max_grade ) )
            

            
            
            ### FILTRAGEM DADOS------------------------------------------------------------------

            ### Variáveis Condicionais
            
            # 1
            ano_construcao = df_clean_f['yr_built'].isin( range(f_ano_construcao[0], f_ano_construcao[1] + 1) )
            
            # 2
            disp = (df_clean_f['date'] >= f_disp[0]) & (df_clean_f['date'] <= f_disp[1])
            
            # 3
            
            price = (df_clean_f['price'] >= f_price[0]) & (df_clean_f['price'] <= f_price[1])
            
            # 4
            
            cond = df_clean_f['condition'].isin( range(f_condition[0], f_condition[1] + 1) )
            
            # 5
            
            grade = df_clean_f['grade'].isin( range(f_grade[0], f_grade[1] + 1) )
            
            
            
            ### Base de Dados sendo filtrada por todos filtros 

            df_filter = df_clean_f[ (ano_construcao) & (disp) & (price) & (cond) & (grade)].reset_index( drop = True )

                    
            # PREPARAÇÃO DE DATASET ----------------------------------------------------------
        
            # Gráfico 3.1 Variação Preço por ano de construção 
            built_grouped = df_filter[['price','yr_built']].groupby(['yr_built']).mean().reset_index()
        
            ## Renomeando Colunas
            built_grouped.columns = ['Ano Construção','Preço Médio']

            
            # Gráfico 3.2 Variação preço médio por data de venda do imóvel
            data_date_grouped = df_filter[['date','price']].groupby(['date']).mean().reset_index()
            
            
            ## Renomeando Colunas
            data_date_grouped.columns = ['Data','Preço Médio']

            
            # Gráfico 3.5 Proporção de imóveis com vista pra água
            
            im_water_grouped = df_filter.drop_duplicates(subset = 'id').loc[:,['id','waterfront']].groupby(['waterfront']).nunique().reset_index()
            
            # Renomeando
            
            im_water_grouped.columns = ['Vista Água','id']
           
            
            # Gráfico 3.7 Proporção de imóveis renovados
            
            
            im_reno_grouped = df_filter.drop_duplicates(subset = 'id').loc[:, ['id','is_renovated']].groupby(['is_renovated']).nunique().reset_index()
            
            
            # Renomeando

            im_reno_grouped.columns = ['Renovado','id']

            ### PLOTAR -------------------------------------------------------------------------
            
            st.header( 'Preço x Ano de Construção' )
            st.markdown('Preço médio por ano de construção')

            
            ## PLOTAR  Gráfico 3.1 Variação Preço por ano de construção
            fig = px.line(built_grouped, x = 'Ano Construção', y = 'Preço Médio' )
            st.plotly_chart(fig, use_container_width= True)
    

    
            st.header( 'Preço x Data venda' )
            st.markdown('Preço médio dos imóveis vendidos por data')
    

            # PLOTAR Gráfico 3.2 Variação preço médio por data de venda do imóvel
            fig = px.line(data_date_grouped, x = 'Data', y = 'Preço Médio' )
            st.plotly_chart(fig, use_container_width= True) 
    
  
    
            st.header( 'Preço x Avaliação Construção' )
            st.markdown('Analisa a variação de preço por classificação da construção dos imóveis na base de dados')
  
    
            # PLOTAR Gráfico 3.3 Análise de Classificação x Preço por boxplot
            fig = px.box(df_filter.rename(columns = {'grade':'Avaliação Construção','price':'Preço'}), x = 'Avaliação Construção', y = 'Preço' )
            st.plotly_chart(fig, use_container_width= True)   
            
            
            c18, c19 = st.columns(( 1 , 1 ))
            
            
            c18.header( 'Preço x Condição' )
            c18.markdown('Analisa a variação de preço por condição dos imóveis na base de dados')
  
            
            # PLOTAR Gráfico 3.4 Análise de Condição x Preço por boxplot
            fig = px.box(df_filter.rename(columns = {'condition':'Condição','price':'Preço'}), x = 'Condição', y = 'Preço' )
            c18.plotly_chart(fig, use_container_width= True) 
    
            c19.header( 'Proporção de imóveis com vista pra água ' )
      
            # PLOTAR Gráfico 3.5 Proporção de imóveis com vista pra água
            fig = px.pie(im_water_grouped, names = 'Vista Água', values = 'id' )
            c19.plotly_chart(fig, use_container_width= True)
            
            c20, c21 = st.columns(( 1 , 1 ))
            
            c20.header( 'Quantidade de imóveis por Preço ' )
      
            # PLOTAR Gráfico 3.6 Quantidade de Imóveis por preço
            fig = px.histogram(df_filter.rename(columns = {'price':'Preço'}), x = 'Preço' )
            c20.plotly_chart(fig, use_container_width= True)
   
            c21.header( 'Proporção de imóveis reformados ' )
      
            # PLOTAR Gráfico 3.7 Proporção de imóveis renovados
            fig = px.pie(im_reno_grouped, names = 'Renovado', values = 'id' )
            c21.plotly_chart(fig, use_container_width= True)
   


    with tab3:
   
        st.header("5 principais insights:")
   
        st.markdown('''Descobertas as quais o time de negócio pode realizar planos de ação (agir) imediato e
                     alinhado com a estratégia do negócio''')      
                     
        
        ### 1 ###
        st.subheader("H1. Imóveis com nível de condição maior ou igual a 3 são 20% mais caras, na média.")

        st.markdown('''**Cenário:** Imóveis com condição maior ou igual a 3 representam 99% dos imóveis listados 
                      na base de dados''') 

        #### TABELA com comparativo de resultados:

        # Preparação:
            
        # Criando dataframa Series para médias de amostras com boas condições e baixas condições   
        im_price_high_cond = df_clean.loc[df['condition'] >= 3 , ['price','price_per_m2_living','price_per_m2_living_outside','m2_living','m2_outside']].mean()
        im_price_low_cond = df_clean.loc[df['condition'] < 3 , ['price','price_per_m2_living','price_per_m2_living_outside','m2_living','m2_outside']].mean()


        ## Passando cada Serie para DataFrame 
        im_price_high_cond = pd.DataFrame(im_price_high_cond)
        im_price_low_cond = pd.DataFrame(im_price_low_cond)

        
        ## Unindo as duas colunas de informações similares
        price_per_condition = pd.concat([im_price_high_cond,im_price_low_cond], axis = 1)

        
        # Definindo nome das colunas da Tabela de Comparação
        price_per_condition.columns = ['Condições Boas','Condições Ruins']
        price_per_condition.index = ['Preço Médio','Preço / área construída (m2) Médio', 'Preço / área construída + externa (m2) Médio','Área Construída (m2) Média', 'Área Externa (m2) Média']


        # Apresentação na tela:
        c22, c23 = st.columns((1.2 , 0.8))
        
        c22.markdown("**Desenvolvimento:**")

        
        c22.markdown("Assumindo que imóveis com boas condições de infraestrutura possuem nota de no mínimo 3.")

        c22.dataframe( price_per_condition )

        #### GRÁFICO com comparativo de resultados:

        ## Transpondo a tabela 
        price_per_condition = price_per_condition.T.reset_index() 
        
        ## Dando nome para coluna de valores que eram coluna 
        price_per_condition.rename(columns = {'index':'Condição'},inplace = True) 


        ## Filtro para selecionar variável a aparecer no gráfico 
        option = c23.selectbox('Compare os atributos:', ('Preço Médio','Preço / área construída (m2) Médio', 'Preço / área construída + externa (m2) Médio','Área Construída (m2) Média', 'Área Externa (m2) Média'))

        ## Plotar gráficos 
        fig = px.bar(price_per_condition, x = 'Condição' , y = option)
        c23.plotly_chart(fig, use_container_width= True)        

        st.markdown('''**Conclusão:** Hipótese **FALSA**''') 

        st.markdown('''- Considerando o **preço médio**, ao invés de 20% mais cara, é 65% mais cara. 

- Porém, se considerar o **preço médio por área construída** são apenas 5% mais caros que os de demais condição. 

> Isso ocorre pois os imóveis com nível de condição maior ou igual a 3 possuem em média área construída 51% maiores que os das demais condições. Dessa forma, o tamanho interno habitável maior acaba penalizando as casas com melhores condições nessa métrica.

- Se acrescentarmos a **área externa** do imóvel no cálculo de preço por área, o preço de imóveis com condição maior ou igual a 3 é maior em 95% dos demais imóveis. 

> Isso ocorre pois os imóveis com nível de condição maior ou igual a 3 possuem, em média, área externa 54% menores que os de demais condições. Então, dessa forma, a métrica de preço por área volta a subir.''') 


        ### 2 ###
        st.subheader("H2. Imóveis com mais de 50 anos com reforma feita são 20% mais caros, em média, que os sem reforma feita.")

        st.markdown('''**Cenário:** Imóveis com idade de 50 anos ou mais que foram renovados representam 8,9% 
                       dos imóveis com mais de 50 anos na base de dados.''') 


        # Preparação:
  
        #### TABELA com comparativo de resultados:
        df_price_renovated = df_clean.loc[ df_clean['age']>= 50 , ['price','price_per_m2_living','m2_living','is_renovated']].groupby('is_renovated').mean().reset_index()

        # Renomeando valores na coluna
        df_price_renovated['is_renovated'].replace( {'Yes':'Sim','No': 'Não'}, inplace = True )
        
        # Definindo nome das colunas da Tabela de Comparação
        df_price_renovated.columns = ['Renovado','Preço Médio','Preço / área construída (m2) Médio', 'Área Construída (m2) Média']
        
        
        # Apresentação na tela:
        c24, c25 = st.columns((1 , 1))
        
        c24.markdown("**Desenvolvimento:**")

        
        #c22.markdown("Assumindo que imóveis com boas condições de infraestrutura possuem nota de no mínimo 3.")

        c24.dataframe( df_price_renovated )

        #### GRÁFICO com comparativo de resultados:           
            
        ## Filtro para selecionar variável a aparecer no gráfico 
        option2 = c25.selectbox('Compare os atributos:', ('Preço Médio','Preço / área construída (m2) Médio', 'Área Construída (m2) Média'))

        ## Plotar gráficos 
        fig = px.bar( df_price_renovated , x = 'Renovado' , y = option2)
        c25.plotly_chart(fig, use_container_width= True)   
        

        st.markdown('''**Conclusão:** Hipótese **FALSA**''') 

        st.markdown('''- Considerando o **preço médio**, ao invés de 20% mais cara, é 53,7% mais cara. 

- Porém, se considerar o **preço médio por área construída**, são apenas 10,7% mais caros que os sem reforma feita. 

> Essa diminuição no preço se explica, pois imóveis com mais de 50 anos com reforma feita possuem área construída 32,2% maior, em média, que os sem reforma feita. ''') 


        ### 3 ###
        st.subheader("H3. Imóveis que possuem vista para água, são 30% mais caros, na média. ")

        st.markdown('''**Cenário:** Imóveis com vista para a água representam 0,7% dos imóveis na base de dados.''') 

        # Preparação:
  
        #### TABELA com comparativo de resultados:
        df_price_waterfront = df_clean[['price', 'price_per_m2_living','price_per_m2_living_outside','m2_living','m2_outside','waterfront']].groupby('waterfront').mean().reset_index()

        # Renomeando valores na coluna
        df_price_waterfront['waterfront'].replace( {'Yes':'Sim','No': 'Não'}, inplace = True )
        
        # Definindo nome das colunas da Tabela de Comparação
        df_price_waterfront.columns = ['Vista Água','Preço Médio','Preço / área construída (m2) Médio', 'Preço / área construída + externa (m2) Médio','Área Construída (m2) Média','Área Externa (m2) Média']
        
        
        # Apresentação na tela:
        c26, c27 = st.columns((1 , 1))
        
        c26.markdown("**Desenvolvimento:**")

        
        #c22.markdown("Assumindo que imóveis com boas condições de infraestrutura possuem nota de no mínimo 3.")

        c26.dataframe( df_price_waterfront )

        #### GRÁFICO com comparativo de resultados:           
            
        ## Filtro para selecionar variável a aparecer no gráfico 
        option3 = c27.selectbox('Compare:', ('Preço Médio','Preço / área construída (m2) Médio', 'Preço / área construída + externa (m2) Médio','Área Construída (m2) Média','Área Externa (m2) Média'))

        ## Plotar gráficos 
        fig = px.bar( df_price_waterfront , x = 'Vista Água' , y = option3)
        c27.plotly_chart(fig, use_container_width= True)   


        st.markdown('''**Conclusão:** Hipótese **FALSA**''') 

        st.markdown('''- Considerando o **preço médio**, ao invés de 30%, são 3x mais caros ou aproximadamente 212,6% mais caros, na média. 

- Porém, se considerar o **preço médio por área construída**, imóveis que possuem vista para água são 93,7% mais caros. 

> Isso é explicado pois imóveis com vista para a água possuem em média 100 m2 a mais de área construída que os sem.

- Se acrescentarmos a **área externa** do imóvel no cálculo de preço por área, o preço de imóveis que possuem vista para água são apenas 42,7% mais caros. 

> Isso é explicado pois imóveis com vista para a água possuem em média 1000 m2 a mais de área externa do terreno que os sem.

> **OBS:** Mesmo retirando o impacto da área ao analisar o fato do imóvel possuir vista para água, a diferença média dos preços ainda é elevada. Outra razão que pode explicar essa grande diferença é a oferta baixa de imnóveis com essa característica.''') 


        ### 4 ###
        st.subheader("H4. Imóveis com data de construção menor que 1955, são 50% mais baratos, na média.")

        st.markdown('''**Cenário:** Imóveis com data de construção menor que 1955 representam 28,4% dos imóveis 
                    listados na base de dados.''') 

        #### TABELA com comparativo de resultados:

        # Preparação:
            
        # Criando dataframa Series para imoveis com ano de construção menores que 1955 e maiores   
        df1 = df_clean.loc[df['yr_built'] < 1955, ['price','price_per_m2_living','price_per_m2_living_outside','m2_living','m2_outside']].mean()
        df2 = df_clean.loc[df['yr_built'] >= 1955, ['price','price_per_m2_living','price_per_m2_living_outside','m2_living','m2_outside']].mean()


        ## Passando cada Serie para DataFrame 
        df1 = pd.DataFrame(df1)
        df2= pd.DataFrame(df2)

        
        ## Unindo as duas colunas de informações similares
        df3 = pd.concat([df1, df2], axis = 1)

        
        # Definindo nome das colunas da Tabela de Comparação
        df3.columns = ['Antigos','Novos']
        df3.index = ['Preço Médio','Preço / área construída (m2) Médio', 'Preço / área construída + externa (m2) Médio','Área Construída (m2) Média', 'Área Externa (m2) Média']


        # Apresentação na tela:
        c28, c29 = st.columns((1.2 , 0.8))
        
        c28.markdown("**Desenvolvimento:**")

        
        c28.markdown("Assumindo que imóveis antigos são imóveis com data de construção menor que 1955.")

        c28.dataframe( df3 )

        #### GRÁFICO com comparativo de resultados:

        ## Transpondo a tabela 
        df3 = df3.T.reset_index() 
        
        ## Dando nome para coluna de valores que eram coluna 
        df3.rename(columns = {'index':'1955'},inplace = True) 


        ## Filtro para selecionar variável a aparecer no gráfico 
        option4 = c29.selectbox('Atributos:', ('Preço Médio','Preço / área construída (m2) Médio', 'Preço / área construída + externa (m2) Médio','Área Construída (m2) Média', 'Área Externa (m2) Média'))

        ## Plotar gráficos 
        fig = px.bar(df3, x = '1955' , y = option4)
        c29.plotly_chart(fig, use_container_width= True)        

        st.markdown('''**Conclusão:** Hipótese **FALSA**''') 

        st.markdown('''- Considerando o **preço médio**, imóveis com data de construção menor que 1955, possuem preços 0,8% mais baratos. 

- Porém, se considerar o **preço médio por área construída**, , imóveis com data de construção menor que 1955 possuem preços 34,4% mais caros, na média. 

> Isso ocorre pois os imóveis com data de construção menor que 1955, possuem área construída 25% menores, na média.

- Se acrescentarmos a **área externa** do imóvel no cálculo de preço por área, imóveis com data de construção menor que 1955, possuem preços 22,65% mais caros, na média. 

> Isso ocorre pois os imóveis com data de construção menor que 1955, possuem área construída 38,75% menores, na média.''') 


        ### 5 ###
        st.subheader("H5. 40% das vendas de imóveis ocorrem no verão.")

        #st.markdown('''**Cenário:** Imóveis com data de construção menor que 1955 representam 28,4% dos imóveis 
        #            listados na base de dados.''') 

        #### TABELA com comparativo de resultados:

        # Preparação:
            
        # Apresentação na tela:
        c30, c31 = st.columns((1 , 1))
        
        c30.markdown("**Desenvolvimento:**")


        #### GRÁFICO com comparativo de resultados:

        ## Plotar gráficos 
        fig = px.histogram(df_clean, x = 'seasons' , title = "Vendas por estação", labels={
                            'count': 'Quantidade', 'seasons': 'Estação'})
        
        c30.plotly_chart(fig, use_container_width= True)        

        c31.markdown('''**Conclusão:** Hipótese **FALSA**''') 

        c31.markdown('''- 29% dos imóveis vendidos ocorrem no verão. 
 - 59% dos imóveis vendidos ocorrem no verão ou primavera.''') 


    with tab4:

        ### 1. PREPARAÇÃO BASE DE DADOS
        
        ## 1.1. Análise de Compra
        
        # Calculo do preço mediano por metro quadrado por região
        df_median_price_m2 = df_clean.drop_duplicates(subset = 'id').loc[:,['zipcode','price_per_m2_living']].groupby('zipcode').median().reset_index()
        
        # Renomear a coluna
        df_median_price_m2.columns = ['zipcode','target_buy']
        
        # Merge com a base de dados geral
        df_compra = df_clean.merge(df_median_price_m2, how = 'left', on = 'zipcode').copy()
        
        ## Aplica fórmula para análise dos imóveis a serem comprados
        df_compra['status'] = df_compra.apply(compra_house, axis = 1)

        ## Ajuste final base de dados de compra - Ordeno pela data mais recente de imóveis e excluo os antigos e colunas desejadas
        df_compra = df_compra.sort_values(by = ['id','date'], ascending = False).drop_duplicates(subset = 'id', keep = 'first', ignore_index = True)

        ## 1.2 Análise de Venda
        
        # Calculo da mediana do preço por metro quadrado de área construída por região por estação - Balizador de regra de preço de venda 
        df_mp_zip_sea = df_clean[['zipcode','price_per_m2_living','seasons']].groupby(['zipcode','seasons']).median().reset_index()
        
        # Renomeando colunas de analise preço balizador para venda
        df_mp_zip_sea.columns = ['zipcode','seasons','median_venda']
        
        # Calculo da media de classificação da qualidade de construção por região - Balizador de regra de preço de venda 
        df_zip_grade = df_compra.loc[:, ['zipcode','grade']].groupby(['zipcode']).mean().reset_index()
        
        # Renomeando colunas 
        df_zip_grade.columns = ['zipcode','mean_grade_per_zip']
        
        # Unir ao dataset completo valores calculados para contribuir para estimar preço de venda
        df_compra_venda = df_compra.merge(df_mp_zip_sea, how = 'left', on = ['zipcode','seasons']).merge(df_zip_grade, how = 'left', on = 'zipcode').copy()
        
        ## Filtrar apenas imóveis que foram comprados e dropar a coluna status
        df_compra_venda = df_compra_venda.loc[df_compra_venda['status'] == 'Compra',:].drop(columns = 'status').reset_index( drop = True )
        
        ## Aplica regras de negócio para estimar preço de venda 
        df_compra_venda['price_venda'] = df_compra_venda.apply(venda_house, axis = 1)
        
        ## Calcula lucro dos imóveis negociados
        df_compra_venda['lucro'] = df_compra_venda['price_venda'] - df_compra_venda['price']
        
        ## Calcula ROI dos imóveis negociados
        df_compra_venda['roi'] = (df_compra_venda['lucro'] / df_compra_venda['price']) * 100
        
        ### 2. APRESENTAÇÃO BASE DE DADOS
        
            
        
        ### 2.1 RECOMENDAÇÕES DE COMPRA - ### Tabelas e Mapas 
        # Ajustar nome das colunas base de dados de compra
        see_data3 = st.expander('Você pode clicar aqui para ver os imóveis recomendados para compra 👉')
        with see_data3:
                
            
            # Trocar nomes das colunas 
            
            df_compra.rename(columns = {'zipcode':'Código Postal','price':'Preço',
                                        'price_per_m2_living':'Preço/m2 construído','target_buy':'Balizador Compra',
                                        'condition':'Condição','grade':'Avaliação Construção','age':'Idade',
                                        'is_renovated':'Reformado'}, inplace = True)
            
            
            # Trocar valores das colunas
            
            df_compra['Reformado'].replace({'No':'Não','Yes':'Sim'}, inplace = True)
            
            
            # Tabela 
            #st.dataframe(df_compra)
            st.dataframe(df_compra[['id','status','Código Postal','Preço','Preço/m2 construído',
                                    'Balizador Compra','Condição','Avaliação Construção','Idade',
                                    'Reformado']].style.applymap( aplic, subset = 'status'))
            
            
                                                                                                                   
                                                
        
        ### 2.2 Filtros e Indicadores
        
        
        ## Arredondar o roi 
        df_compra_venda["roi"] = df_compra_venda["roi"].round(2)
               
                   
        c32, c33, c34, c35, c36 = st.columns((1,1,1,1,1))
        
        ### Valor de ROI desejado para o investimento       
        min_roi = int(df_compra_venda["roi"].min())
        max_roi = int(df_compra_venda["roi"].max())
        
        
        
        f_roi = c32.slider('Retorno sob investimento desejado:', min_value = min_roi, max_value = max_roi,
                                                               value = ( min_roi , max_roi ) )
        
        
        ## Seleção de dados pelo roi 
        df_compra_venda = df_compra_venda.loc[ (df_compra_venda['roi'] >= f_roi[0]) & (df_compra_venda['roi'] <= f_roi[1])  , :]
        
        ### Indicadores - (Quantidade de Imóveis - Lucro Total - ROI médio)
        
        lucro_total = df_compra_venda.loc[:, 'lucro'].sum()
        
        roi_mean = df_compra_venda.loc[:, 'roi'].mean()
        
        c34.metric(label="🏠 Quantidade Imóveis", value = str(df_compra_venda.loc[:, 'id'].count()))
        c35.metric(label= "💰Lucro Total", value = 'R$' + '{:.2f}'.format(lucro_total))
        c36.metric(label= "↩️ ROI médio", value = '{:.2f}'.format(roi_mean) + "%")
        
                   
        ### 2.3 RETORNO INVESTIMENTO - Tabelas e Mapas
        see_data4 = st.expander('Você pode clicar aqui para ver os retornos esperados dos imóveis recomendados 👉')
        with see_data4:  
            
            # Trocar nomes das colunas e valores se desejar  
            
            # Trocar nomes das colunas 
            
            df_compra_venda.rename(columns = {'zipcode':'Código Postal','price':'Preço Compra',
                                              'seasons':'Estação','price_per_m2_living':'Preço/m2 construído',
                                              'target_buy':'Balizador Compra','condition':'Condição',
                                              'grade':'Avaliação Construção','age':'Idade',
                                              'is_renovated':'Reformado','median_venda': 'Balizador Venda',
                                              'mean_grade_per_zip':'Média Avaliação por Código Postal', 
                                              'price_venda':'Preço Venda estimado', 'lucro':'Lucro estimado',
                                              'roi':'ROI estimado', 'm2_living':'Área construída(m2)'}, inplace = True)
            
            
            # Trocar valores das colunas
            
            df_compra_venda['Reformado'].replace({'No':'Não','Yes':'Sim'}, inplace = True)
            
            
            
            
            
            # Tabela
            st.dataframe(df_compra_venda[['id','Código Postal','Preço Compra','Preço/m2 construído', 'Área construída(m2)',
                                    'Condição','Avaliação Construção','Reformado','Estação', 'Balizador Venda',
                                    'Média Avaliação por Código Postal','Preço Venda estimado',
                                    'Lucro estimado','ROI estimado']])
            
            
            # Plotar mapa de calor - Lucro médio por região com os investimentos estimados
            
            ## Preparação Mapas
            
            data_map = df_compra_venda[['Lucro estimado','Código Postal']].groupby( ['Código Postal'] ).mean().reset_index() 
    
            data_map.columns = ['ZIP', 'LUCRO']
        
    
            # Filtrar do arquivo com as coordenadas de regiões totais apenas as regiões de amostra que peguei para analisar preço médio no dataset 
            # para depois não acabar ficando regiões sem dado de preço médio
            geofile = geofile[geofile['ZIP'].isin( data_map['ZIP'].tolist() )]
    
            # Mapa Base - Folium - é apenas o mapa sem pontos
            region_lucro = folium.Map( location= [df_clean['lat'].mean(), df_clean['long'].mean() ], 
                                       default_zoom_start=15 )
    
    
            folium.Choropleth( data = data_map, geo_data = geofile, columns=['ZIP', 'LUCRO'],
                                 key_on='feature.properties.ZIP', fill_color='YlOrRd',
                                 fill_opacity = 0.7, line_opacity = 0.2,
                                 legend_name='MÉDIA LUCRO' ).add_to(region_lucro)
            
            
            
            # Preparação mapa Distribuição/Densidade dos imóveis investidos
            
            #data_map = df.sample( 10 ) # Pegar apenas 10 amostras de imóveis
    
            # Mapa Base - Folium - é apenas o mapa sem pontos
            density_map_compra = folium.Map( location=[df_clean['lat'].mean(), df_clean['long'].mean() ], 
                                             default_zoom_start=15 )
    
    
            # Instanciando objeto para inserir os dados de imóveis no mapa, os pontos
            marker_cluster = MarkerCluster().add_to( density_map_compra )
    
            # Inserção dos pontos imóveis no mapa transformando dataframe com dados em iterativo para usar o for com estruturas dataframe
            # row = linha -> imóveis/amostra/observação distinta
            # popup = descrição ao passar o mouse sobre os pontos
            for name, row in df_compra_venda.iterrows():
        
                folium.Marker( [row['lat'], row['long'] ], popup='''Preço estimado de venda: ${0:.2f}, 
                                                                    Lucro: ${1:.2f}, ROI: {2:.2f}%.                                                                     
                                                                  Características: {3:.2f} m2 de área construída, 
                                                                  {4} quartos,{5} banheiros, 
                                                                  ano construção: {6}.'''.format( row['Preço Venda estimado'],
                                                                                                  row['Lucro estimado'],
                                                                                                  row['ROI estimado'],
                                                                                                  row['Área construída(m2)'],
                                                                                                  row['bedrooms'],
                                                                                                  row['bathrooms'],
                                                                                                  row['yr_built'] ) ).add_to( marker_cluster )
            
            
            
            ## Plot dos mapas
            
            
            
            c32, c33 = st.columns((1,1))
            
            
            with c32:
            
            
                st.header( 'Lucro médio por região' )
                folium_static( region_lucro ) 

       
            with c33:
            
                # Plotar mapa Distribuição/Densidade dos imóveis investidos 
                
                st.header( 'Imóveis investidos' )
                folium_static(density_map_compra) 



#================================================================================ 
## Transform ###-------------------------------------------------------------------
#================================================================================

#================================================================================
## Load ###-------------------------------------------------------------------
#================================================================================

# Para testar variáveis
#st.write(f'zc:{f_zip_code}')
#st.write(f'colunas:{f_colunas}')

    ## ===================================================================
    ## 1. Data Overview
    ## ===================================================================
    # ==============================================
    # 2. Mapa de distribuição e preço 
    # ==============================================

    # ==============================================
    # 3. Preço no tempo 
    # ==============================================

    # ===================================================
    # 4. Distribuição de imóveis por atributo 
    # ===================================================

