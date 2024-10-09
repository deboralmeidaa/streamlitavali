import pandas as pd 
import numpy as np 
import plotly.express as px
import streamlit as st 

# DADOS
casos=pd.read_csv("SERIES_CASOS_BAIRRO.csv",sep=";")
casos['DATA']=pd.to_datetime(casos['DATA'])
casos["FORTALEZA"]=casos.drop("DATA",axis=1).sum(axis=1)

mortes=pd.read_csv("SERIES_OBITOS_BAIRRO.csv",sep=";")
mortes['DATA']=pd.to_datetime(mortes['DATA'])
mortes["FORTALEZA"]=mortes.drop("DATA",axis=1).sum(axis=1)

lista_locais=list(casos.drop("DATA",axis=1).columns)


st.title("Analise Covid - Fortaleza")

option = st.selectbox(
    "Selecione sua região para analise",
    lista_locais
)
local=option
casos_local=casos[local].sum()
mortes_local=mortes[local].sum()


with st.sidebar:
        seletor=st.selectbox(
    "Selecione o tipo do dado",["CASOS E MORTES","CASOS","MORTES"]
)

figcasos=px.line(casos,x="DATA",y=local,labels={local:"CASOS"})
figmortes=px.line(mortes,x="DATA",y=local,labels={local:"MORTES"})

if seletor=="CASOS E MORTES":
        col1, col2= st.columns(2)
        col1.metric("CASOS:", casos_local)
        col2.metric("MORTES",mortes_local )
        st.plotly_chart(figcasos)
        st.plotly_chart(figmortes)
        
if seletor=="CASOS":
        col1= st.columns(1)
        col1.metric("CASOS:", casos_local)
        st.plotly_chart(figcasos)
        
if seletor=="MORTES":
        col1= st.columns(1)
        col1.metric("MORTES:", mortes_local)
        st.plotly_chart(figmortes)
 






