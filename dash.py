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
    graf1, graf2, graf3, graf4, graf5 = st.tabs(['Gráfico de Barras', 
                                                 'Gráfico de Linhas', 
                                                 'Gráficos de Pizza', 
                                                 'Gráfico de Dispersão',
                                                 'Gráfico de Área'])
    
    with graf1:
        st.write('Gráfico de Barras')
        
        investimento = df_selecionado.groupby('marca').count()[['valor']].sort_values(by='valor', ascending=False)
        # Agrupar pela marca e conta o numero de ocorrencias da coluna valor. Depois ordena o resultado de forma decrescente
        
        fig_valores = px.bar(investimento, # Dados que serão utilizados no gráfico
                             x=investimento.index, 
                             y='valor', orientation='v', 
                             title='<b>Valores de Carros</b>', 
                             color_discrete_sequence=['#0083b3']
                             )
        
        st.plotly_chart(fig_valores, use_container_width=True)
    
    with graf2:
        st.write('Gráfico de linhas')
        dados = df_selecionado.groupby('marca').count()[['valor']]
        
        fig_valores2 = px.line(dados,
                               x=dados.index,
                               y='valor',
                               title='<b>Valores por Marca</b>',
                               color_discrete_sequence=['#0083b3']
                               )
        
        st.plotly_chart(fig_valores2, use_container_width=True)
    
    with graf3:
        st.write('Gráficos de Pizza')
        dados2 = df_selecionado.groupby('marca').sum()[['valor']]
        
        fig_valores3 = px.pie(dados2,
                              values='valor', # Valores que serão representados
                              names=dados2.index, # Os nomes (marcas) que irão rotular
                              title='<b>Distribuição de valores por marca</b>'
                              )
        
        st.plotly_chart(fig_valores3, use_container_width=True)
                
        dados_vendas = df_selecionado.groupby('marca').sum()[['numero_vendas']]
        
        fig_valores3 = px.pie(dados_vendas,
                              values='numero_vendas', # Valores que serão representados
                              names=dados_vendas.index, # Os nomes (marcas) que irão rotular
                              title='<b>Distribuição de vendas por marca</b>'
                              )
        
        st.plotly_chart(fig_valores3, use_container_width=True)
        
        
        
    with graf4:
        st.write('Gráfico de Dispersão')
        dados3 = df_selecionado.melt(id_vars=['marca'], value_vars=['valor'])
        
        fig_valores4 = px.scatter(dados3,
                                  x='marca',
                                  y='value',
                                  color='variable',
                                  title='<b>Dispersão de valores por marca</b>'
                                  )
        
        st.plotly_chart(fig_valores4, use_container_width=True)

    with graf5:
        st.write('Gráfico de Área')
        dados4 = df_selecionado.melt(id_vars=['marca'], value_vars=['valor'])
        
        st.area_chart(dados4,
                      x='marca',
                      y='value',
                      )
 
        
def barra_progresso():
    valor_atual = df_selecionado['numero_vendas'].sum()
    objetivo = 20000000
    percentual = round((valor_atual/objetivo * 100))
    
    if percentual > 100:
        st.subheader('Valores Atingidos!!!')
    else:
        st.write(f'Você tem {percentual}% de {objetivo}. Vai atrás paezão!')
        mybar = st.progress(0)
        for percentual_completo in range(percentual):
            mybar.progress(percentual_completo + 1, text='Alvo %')
            
            
# ********* MENU LATERAL *************
def menu_lateral():
    with st.sidebar:
        selecionado = option_menu(menu_title='Menu', 
                                options=['Home', 'Progresso'],
                                icons=['house', 'eye'],
                                menu_icon='cast',
                                default_index=0
                                )
        
    if selecionado == 'Home':
        st.subheader(f'Página: {selecionado}')
        Home()
        graficos(df_selecionado)
        
    if selecionado == 'Progresso':
        st.subheader(f'Página: {selecionado}')
        barra_progresso()
        graficos(df_selecionado)


# ********* Ajustar o CSS ********



menu_lateral()