# pip install streamlit

import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from query import conexao

# *** PRIMEIRA CONSULTA / ATUALIZAÇÕES DOS DADOS ***
query = 'SELECT * FROM tb_carros'

# Carregar os dados 
df = conexao(query)

# Botao para atualizar
if st.button('Atualizar Dados'):
    df = conexao(query)
    
# ***** Estrututra Lateral de Filtros *****
st.sidebar.header('Selecione o Filtro')

marca = st.sidebar.multiselect('Marca Selecionada', # Nome do seletor
                               options=df['marca'].unique(), # Opções 
                               default=df['marca'].unique() # Valores padrão
                               )

modelo = st.sidebar.multiselect('Modelo Selecionado', # Nome do seletor
                               options=df['modelo'].unique(), # Opções 
                               default=df['modelo'].unique() # Valores padrão
                               )

valor = st.sidebar.multiselect('Valor Selecionada', # Nome do seletor
                               options=df['valor'].unique(), # Opções 
                               default=df['valor'].unique() # Valores padrão
                               )

cor = st.sidebar.multiselect('Cor Selecionada', # Nome do seletor
                               options=df['cor'].unique(), # Opções 
                               default=df['cor'].unique() # Valores padrão
                               )

numero_vendas = st.sidebar.multiselect('Número de Vendas Selecionada', # Nome do seletor
                               options=df['numero_vendas'].unique(), # Opções 
                               default=df['numero_vendas'].unique() # Valores padrão
                               )

ano = st.sidebar.multiselect('Ano Selecionado', # Nome do seletor
                               options=df['ano'].unique(), # Opções 
                               default=df['ano'].unique() # Valores padrão
                               )


# Aplicar os filtros selecionados
df_selecionado = df[
    (df['marca'].isin(marca)) &
    (df['modelo'].isin(modelo)) &
    (df['ano'].isin(ano)) &
    (df['valor'].isin(valor)) &
    (df['cor'].isin(cor)) &
    (df['numero_vendas'].isin(numero_vendas))
]

# **** Exibir Valores médios - estatistica
def Home():
    with st.expander('Valores'): # Cria uma caixa expansivel com um titulo
        mostrarDados = st.multiselect('Filter: ', df_selecionado, default=[])
        
        # Verifica se o usuario selecionou uma coluna para exibir
        if mostrarDados:
            # Exibe os dados filtrados pelas colunas selecionadas
            st.write(df_selecionado[mostrarDados])
    
    if not df_selecionado.empty:
        venda_total =  df_selecionado['numero_vendas'].sum()
        venda_media = df_selecionado['numero_vendas'].mean()
        venda_mediana = df_selecionado['numero_vendas'].median()
        
        # Cria tres colunas para exibir os totais calculados
        total1, total2, total3 = st.columns(3, gap='large')
        
        with total1:
            st.info('Valor total de vendas dos carros', icon='📌')
            st.metric(label='Total', value=f'{venda_total:,.0f}')
            
        with total2:
            st.info('Valor médio das vendsa', icon='📌')
            st.metric(label='Média', value=f'{venda_media:,.0f}')
            
        with total3:
            st.info('Valor mediana dos carros', icon='📌')
            st.metric(label='Mediana', value=f'{venda_mediana:,.0f}')
    
    else:
        st.warning('Nenhum dado disponível com os filtros selecionados')
    
    st.markdown('''--------''')   
    
    
# Graficos

def graficos(df_selecionado):
    # Verifica se o dataframe está vazio
    if df_selecionado.empty:
        st.warning('Nenhum dado disponível para gerar gráficos')
        return
    
    # Criação dos gráficos
    graf1, graf2, graf3, graf4 = st.tabs(['Gráfico de Barras', 'Gráfico de Linhas', 'Gráfico de Pizza', 'Gráfico de Dispersão'])
    
    
Home()