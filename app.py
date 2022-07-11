import streamlit as st
import requests
import pandas as pd
import plotly.express as px
base="dark"
backgroundColor="#652e69"

st.set_page_config(layout="wide",
                   page_icon="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png",
                   page_title = "Web app Diplomado")

@st.cache
def cargar_datos(filename: str):
    return pd.read_csv(filename)

datos = cargar_datos("Cordoba_limpio.csv")
# Sidebar
st.sidebar.image("logo-DANE.png")
st.sidebar.markdown("# Seleccion de estrato, para el departamento de cordoba, en todos los municipios")
st.sidebar.markdown("---")
estrato = st.sidebar.selectbox(
    label = "Estrato", options=['1','2','3','4','5','6'])
st.sidebar.markdown("---")
st.sidebar.markdown("# Selector de opcion para Grafico 2")
opcionPie = st.sidebar.selectbox(label="Servicios basicos", 
                                 options =["descripcion_tipo_vivienda","descripcion_material_pared","descripcion_tipo_servicio_sanitario"])

st.header("Datos de referecia utilizado para la prediccion de precios")
st.markdown("---")
st.write(datos)
st.markdown("---")
st.markdown("Figura 1.")

@st.cache
def graficobarras(datos):
    
    fig = px.bar(
        datos.groupby(["estrato"])
        .sum()
        .reset_index()
        .sort_values(by="total_hogares", ascending=False),
        color_discrete_sequence=["#B0C4DE","white"],
        x ="estrato",
        y ="total_hogares"
    )
    return fig
varfig = graficobarras(datos)
st.plotly_chart( 
    varfig , 
    use_container_width=True,  
)

st.markdown("---")

st.markdown("# Grafico 2")
@st.cache
def pieFig(df,x):
    sizes = datos[x].value_counts().tolist()
    labels = datos[x].unique()
    return [sizes,labels]
fig = px.pie(datos, 
             values=pieFig(datos,opcionPie)[0], 
             names=pieFig(datos,opcionPie)[1], 
             title='Informacion Adicional del censo realizado',
            color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig)