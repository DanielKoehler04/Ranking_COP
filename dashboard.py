import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Ranking COP", layout="wide")
st.title("Ranking COP")

url = "https://docs.google.com/spreadsheets/d/1cT8Lwp49xedjsHgXuu0KEmS_FzB18gYpyIV1UDxJTUk/gviz/tq?tqx=out:csv"
df = pd.read_csv(url, on_bad_lines='skip')

st.sidebar.header("Filtros")

servs = ["Todos", "Adesões", "Reparos", "Serviços"]

servico_escolhido = st.sidebar.selectbox("Selecione a categoria", servs )




top_agendamento = df[df["TIPO PROD"] == "AGENDAMENTO"].iloc[0]
top_controlador =  df[df["TIPO PROD"] == "CONTROLE"].iloc[0]

st.markdown(
    """
    <style>
    @keyframes float{
        0%, 100%{
            transform: translateY(-0rem);
        }
        50%{
            transform: translateY(-0.5rem);
        }
    }

    .center-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 40px; /* espaçamento entre cards */
        flex-wrap: wrap; /* se a tela for pequena, quebra linha */
        margin-top: 10px;
        maring-bottom: 100px
    }
    .card {
        
        padding: 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 12px #3F3E3E;
      
        transition: 0.3s;
        margin-bottom:100px;
        animation: float 2.5s ease-in-out infinite;
    }
   
    .card img {
        border-radius: 50%;
        margin-bottom: 12px;
    }
    .title {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 8px;
        color: white1;
    }
    .value {
        font-size: 16px;
        font-weight: 500;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="center-container">
        <div class="card">
            <h4>🏅 Top Agendamento</h4>
            <img src="https://randomuser.me/api/portraits/men/52.jpg" width="100">
            <div class="title">{top_agendamento['MAIOR PRODUTIVA']}</div>
            <div class="value">{top_agendamento['TOTAL PRODUTIVAS'].astype(int)} Produtivas</div>
        </div>
        <div class="card">
            <h4>🎖️ Top Controlador</h4>
            <img src="https://randomuser.me/api/portraits/women/60.jpg" width="100">
            <div class="title">{top_controlador['MAIOR PRODUTIVA']}</div>
            <div class="value">{top_controlador['TOTAL PRODUTIVAS'].astype(int)} Produtivas</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)




graficos = [
    "PRODUTIVAS TOTAL",
    "IMPRODUTIVAS TOTAL",
    "PRODUTIVAS ADESÃO",
    "IMPRODUTIVAS ADESÃO",
    "PRODUTIVAS REPARO",
    "IMPRODUTIVAS REPARO",
    "PRODUTIVAS SERVIÇO",
    "IMPRODUTIVAS SERVIÇO"
]

def gera_grafico(grafico):
    fig = px.bar(df, x="NOME", y=grafico, color="TIPO", text=grafico, title=grafico)
    
    fig.update_layout(
        autosize = True,
        width=None,
        template="ggplot2",
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        margin=dict(t=30, b=0)
    )
    fig.update_yaxes(automargin=True)

    fig.update_traces(
        textposition="outside",  # ou "top center"
        textfont=dict(size=14),
    )


    st.plotly_chart(fig, use_container_width=True)



col1, col2 = st.columns(2)

fig_rank1 = px.bar(df, x='MAIOR PRODUTIVA', y="TOTAL PRODUTIVAS", color="TIPO PROD", text="TOTAL PRODUTIVAS", title="MAIORES PRODUTIVAS ✅")
fig_rank1.update_traces(
        textposition="outside",  # ou "top center"
        textfont=dict(size=14),
    )
fig_rank1.update_layout(
        autosize = True,
        width=None,
        template="ggplot2",
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        margin=dict(t=30, b=0)
    )

col1.plotly_chart(fig_rank1, use_container_width=True)

fig_rank2 = px.bar(df, x="MAIOR IMPRODUTIVA", y="TOTAL IMPRODUTIVAS", color="TIPO IMPRO", text="TOTAL IMPRODUTIVAS", title="MAIORES IMPRODUTIVAS ❌")
fig_rank2.update_traces(
        textposition="outside",  # ou "top center"
        textfont=dict(size=14),
    )
fig_rank2.update_layout(
        autosize = True,
        width=None,
        template="ggplot2",
        uniformtext_minsize=8,
        uniformtext_mode="hide",
        margin=dict(t=30, b=0)
    )


col2.plotly_chart(fig_rank2, use_container_width=True)

st.title("Valores Gerais")



if servico_escolhido == servs[0]:
    for i in graficos[:2]:
        gera_grafico(i)
if servico_escolhido == servs[1]:
    for i in graficos[2:4]:
        gera_grafico(i)
if servico_escolhido == servs[2]:
    for i in graficos[4:6]:
        gera_grafico(i)
if servico_escolhido == servs[3]:
    for i in graficos[6:8]:
        gera_grafico(i)
        




