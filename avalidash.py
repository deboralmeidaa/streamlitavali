import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import seaborn as sns

st.set_page_config(layout="wide")

def count_palavras(texto):
    return len(texto.split())


# IBYTE 
ibyte = pd.read_csv("RECLAMEAQUI_IBYTE.csv")
ibyte['TEMPO']=pd.to_datetime(ibyte['TEMPO'])

estado_lista_ibyte=[]
for i in range(len(ibyte)):
    estado_lista_ibyte.append(ibyte['LOCAL'].iloc[i].split('-',2)[1].strip())

ibyte['ESTADO']=estado_lista_ibyte

correcao_estados_ibyte = {
    'Mirim': 'RN',
    'P': 'PE',
    'C': 'CE',
    '': 'Não Consta',
    'naoconsta': 'Não Consta'  
}

ibyte['ESTADO'] = ibyte['ESTADO'].replace(correcao_estados_ibyte)


# NAGEM
nagem = pd.read_csv("RECLAMEAQUI_NAGEM.csv")
nagem['TEMPO'] = pd.to_datetime(nagem['TEMPO'])

estado_lista_nagem=[]
for i in range(len(nagem)):
    estado_lista_nagem.append(nagem['LOCAL'].iloc[i].split('-',2)[1].strip())

nagem['ESTADO'] = estado_lista_nagem

correcao_estados_nagem = {
    'naoconsta': 'Não Consta',
    '': 'Não Consta'
}

nagem['ESTADO'] = nagem['ESTADO'].replace(correcao_estados_nagem)


# HAPVIDA
hapvida = pd.read_csv("RECLAMEAQUI_HAPVIDA.csv")
hapvida['TEMPO'] = pd.to_datetime(hapvida['TEMPO'])

estado_lista_hapvida=[]
for i in range(len(hapvida)):
    estado_lista_hapvida.append(hapvida['LOCAL'].iloc[i].split('-',2)[1].strip())

hapvida['ESTADO'] = estado_lista_hapvida

correcao_estados_hapvida = {
    '': 'Não Consta'
}

hapvida['ESTADO'] = hapvida['ESTADO'].replace(correcao_estados_hapvida)


# DASHBOARD
lista_loja = ["HAPVIDA","NAGEM","IBYTE"]
lista_painel = ["Série Temporal do Número de Reclamações","Frequência de Reclamações por Estado","Frequência de Status","Distribuição do Tamanho do Texto"]

col1,col2 = st.columns(spec=[0.2,0.8],gap="large")

with col1:
    st.subheader("RECLAME AQUI",divider="gray")

    loja_selecionada = st.selectbox(
        "Selecione uma empresa:",
        lista_loja
    )

with col2:

    if loja_selecionada == "HAPVIDA":
        st.title("HAPVIDA")
    elif loja_selecionada == "NAGEM":
        st.title("NAGEM")
    elif loja_selecionada == "IBYTE":
        st.title("IBYTE")

    tab1,tab2,tab3,tab4 = st.tabs(lista_painel)

    # Série Temporal do Número de Reclamações
    with tab1:
        if loja_selecionada == "IBYTE":
            
            agrupado_ibyte = ibyte.groupby('TEMPO')['ID'].nunique().reset_index()
            temporal_ibyte = px.line(agrupado_ibyte, x='TEMPO', y='ID', labels={'ID': '', 'TEMPO': 'Tempo'}, title="Série temporal do número de reclamações")

            st.plotly_chart(temporal_ibyte)   
        elif loja_selecionada == "NAGEM":

            agrupado_nagem = nagem.groupby('TEMPO')['ID'].nunique().reset_index()
            temporal_nagem = px.line(agrupado_nagem, x='TEMPO', y='ID', labels={'ID': '', 'TEMPO': 'Tempo'}, title="Série temporal do número de reclamações")

            st.plotly_chart(temporal_nagem)
        elif loja_selecionada == "HAPVIDA":
            
            agrupado_hapvida = hapvida.groupby('TEMPO')['ID'].nunique().reset_index()
            temporal_hapvida = px.line(agrupado_hapvida, x='TEMPO', y='ID', labels={'ID': '', 'TEMPO': 'Tempo'}, title="Série temporal do número de reclamações")

            st.plotly_chart(temporal_hapvida) 

    # Frequência de Reclamações por Estado
    with tab2:
        if loja_selecionada == "IBYTE":

            freq_estado_ibyte = ibyte['ESTADO'].value_counts().reset_index()
            freq_estado_ibyte.columns = ['ESTADO', 'Frequencia']
            estado_ibyte = px.bar(freq_estado_ibyte, x='ESTADO', y='Frequencia', title='Frequência por Estado', labels={'Frequencia': 'Contagem'})
            
            st.plotly_chart(estado_ibyte)

            estados_ibyte = ibyte['ESTADO'].unique()
            estado_select_ibyte = st.selectbox("Selecione o estado:", estados_ibyte)

            ibyte_filtrado = ibyte[ibyte['ESTADO'] == estado_select_ibyte]
            ibyte_filtrado = ibyte_filtrado.reset_index(drop=True)
            
            st.dataframe(ibyte_filtrado)   
        elif loja_selecionada == "NAGEM":

            freq_estado_nagem = nagem['ESTADO'].value_counts().reset_index()
            freq_estado_nagem.columns = ['ESTADO', 'Frequencia']
            estado_nagem = px.bar(freq_estado_nagem, x='ESTADO', y='Frequencia', title='Frequência por Estado', labels={'Frequencia': 'Contagem'})

            st.plotly_chart(estado_nagem)

            estados_nagem = nagem['ESTADO'].unique()
            estado_select_nagem = st.selectbox("Selecione o estado:", estados_nagem)

            nagem_filtrado = nagem[nagem['ESTADO'] == estado_select_nagem]
            nagem_filtrado = nagem_filtrado.reset_index(drop=True)

            st.dataframe(nagem_filtrado)
        elif loja_selecionada == "HAPVIDA":

            freq_estado_hapvida = hapvida['ESTADO'].value_counts().reset_index()
            freq_estado_hapvida.columns = ['ESTADO', 'Frequencia']
            estado_hapvida = px.bar(freq_estado_hapvida, x='ESTADO', y='Frequencia', title='Frequência por Estado', labels={'Frequencia': 'Contagem'})

            st.plotly_chart(estado_hapvida)

            estados_hapvida = hapvida['ESTADO'].unique()
            estado_select_hapvida = st.selectbox("Selecione o estado:", estados_hapvida)

            hapvida_filtrado = hapvida[hapvida['ESTADO'] == estado_select_hapvida]
            hapvida_filtrado = hapvida_filtrado.reset_index(drop=True)
            st.dataframe(hapvida_filtrado)

    # Frequência de Status
    with tab3:
        if loja_selecionada == "IBYTE":

            freq_ibyte = ibyte['STATUS'].value_counts().reset_index()
            freq_ibyte.columns = ['STATUS', 'Frequencia']
            status_ibyte = px.bar(freq_ibyte, x='STATUS', y='Frequencia', title='Frequência dos Status', labels={'Frequencia': 'Contagem'})

            st.plotly_chart(status_ibyte)
            st.table(freq_ibyte)

            status_op_ibyte = ibyte['STATUS'].unique().tolist()
            select_status_ibyte = st.selectbox('Selecione o Status:', status_op_ibyte)

            ibyte_filtrado_status = ibyte[ibyte['STATUS'] == select_status_ibyte]

            ibyte_filtrado_status = ibyte_filtrado_status.reset_index(drop=True)

            st.dataframe(ibyte_filtrado_status)
        elif loja_selecionada == "NAGEM":

            freq_nagem = nagem['STATUS'].value_counts().reset_index()
            freq_nagem.columns = ['STATUS', 'Frequencia']
            status_nagem = px.bar(freq_nagem, x='STATUS', y='Frequencia', title='Frequência dos Status', labels={'Frequencia': 'Contagem'})

            st.plotly_chart(status_nagem)
            st.table(freq_nagem)

            status_op_nagem = nagem['STATUS'].unique().tolist()
            select_status_nagem = st.selectbox('Selecione o Status:', status_op_nagem)

            nagem_filtrado_status = nagem[nagem['STATUS'] == select_status_nagem]

            nagem_filtrado_status = nagem_filtrado_status.reset_index(drop=True)

            st.dataframe(nagem_filtrado_status)
        elif loja_selecionada == "HAPVIDA":

            freq_hapvida = hapvida['STATUS'].value_counts().reset_index()
            freq_hapvida.columns = ['STATUS', 'Frequencia']
            status_hapvida = px.bar(freq_hapvida, x='STATUS', y='Frequencia', title='Frequência dos Status', labels={'Frequencia': 'Contagem'})

            st.plotly_chart(status_hapvida)
            st.table(freq_hapvida)

            status_op_hapvida = hapvida['STATUS'].unique().tolist()
            select_status_hapvida = st.selectbox('Selecione o Status:', status_op_hapvida)

            hapvida_filtrado_status = hapvida[hapvida['STATUS'] == select_status_hapvida]

            hapvida_filtrado_status = hapvida_filtrado_status.reset_index(drop=True)

            st.dataframe(hapvida_filtrado_status)
    
    # Distribuição do Tamanho do Texto
    with tab4:
        if loja_selecionada == "IBYTE":

            ibyte['num_palavras'] = ibyte['DESCRICAO'].apply(count_palavras)

            plt.figure(dpi=150)
            sns.histplot(ibyte['num_palavras'], bins=10, kde=True, stat='density')
            plt.title('Gráfico de Distribuição do Tamanho do Texto')
            plt.xlabel('Número de Palavras')

            st.pyplot(plt)
        elif loja_selecionada == "NAGEM":

            nagem['num_palavras'] = nagem['DESCRICAO'].apply(count_palavras)

            plt.figure(dpi=150)
            sns.histplot(nagem['num_palavras'], bins=10, kde=True, stat='density')
            plt.title('Gráfico de Distribuição do Tamanho do Texto')
            plt.xlabel('Número e Palavras')

            st.pyplot(plt)
        elif loja_selecionada == "HAPVIDA":

            hapvida['num_palavras'] = hapvida['DESCRICAO'].apply(count_palavras)

            plt.figure(dpi=150)
            sns.histplot(hapvida['num_palavras'], bins=10, kde=True, stat='density')
            plt.title('Gráfico de Distribuição do Tamanho do Texto')
            plt.xlabel('Número e Palavras')

            st.pyplot(plt)




