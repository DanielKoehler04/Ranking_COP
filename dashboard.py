import pandas as pd
import streamlit as st
import plotly.express as px
import datetime
import streamlit_authenticator as stauth
import base64

st.set_page_config(page_title="Ranking COP", layout="wide")
st.title("Ranking COP")

credentials = {
  "usernames": {
    "daniel": {"name":"Daniel", "password":"1234"},
    "base27": {"name":"Base27", "password":"base27"}
  }
}

auth = stauth.Authenticate(credentials, "cookie_name", "signature_key", cookie_expiry_days=30)

auth.login(location="sidebar")

authentication_status = st.session_state["authentication_status"]
name = st.session_state.get("name")
username = st.session_state.get("username")

st.markdown("""
    <style>
    div[data-testid="stMarkdownContainer"] p {
        font-size: 20px;  
    }
    </style>
""", unsafe_allow_html=True)

if authentication_status:
    st.sidebar.success(f"Bem-vindo, {st.session_state['name']}!")
    auth.logout("Sair", "sidebar")
    

    data_atual = datetime.date.today()

    url = "https://docs.google.com/spreadsheets/d/1cT8Lwp49xedjsHgXuu0KEmS_FzB18gYpyIV1UDxJTUk/gviz/tq?tqx=out:csv"
    df = pd.read_csv(url, on_bad_lines='skip')

    st.sidebar.header("Filtros")

    servs = ["Todos", "Adesões", "Reparos", "Serviços"]

    servico_escolhido = st.sidebar.selectbox("Selecione a categoria", servs )

    
    top_controlador_diario = df[df["TIPO"] == "CONTROLE"].copy()
    top_controlador_mes = df[df["TIPO MES"] == "CONTROLE"].copy()
    
    top_controlador_diario["VALOR DIARIO"] = pd.to_numeric(top_controlador_diario["VALOR DIARIO"], errors="coerce")
    menor_valor_cont = top_controlador_diario["VALOR DIARIO"].min()
    menores_cont = top_controlador_diario[top_controlador_diario["VALOR DIARIO"] == menor_valor_cont][["NOME", "VALOR DIARIO"]]
    menores_acumulado_cont = top_controlador_diario[top_controlador_diario["VALOR DIARIO"] == menor_valor_cont][["NOME", "IMPRODUTIVAS TOTAL", "VALOR DIARIO"]]
    menor_acumulado_cont = menores_acumulado_cont["IMPRODUTIVAS TOTAL"].min()
    top_dia_cont = top_controlador_diario[top_controlador_diario["IMPRODUTIVAS TOTAL"] == menor_acumulado_cont][["NOME", "IMPRODUTIVAS TOTAL", "VALOR DIARIO"]].iloc[0]


   
    
    top_agendamento_diario = df[df["TIPO"] == "AGENDAMENTO"].copy()
    top_agendamento_mes = df[df["TIPO MES"] == "AGENDAMENTO"].copy()

    top_agendamento_diario["VALOR DIARIO"] = pd.to_numeric(top_agendamento_diario["VALOR DIARIO"], errors="coerce")
    menor_valor_ag = top_agendamento_diario["VALOR DIARIO"].min()
    menores_ag = top_agendamento_diario[top_agendamento_diario["VALOR DIARIO"] == menor_valor_ag][["NOME", "VALOR DIARIO"]]
    menores_acumulado_ag = top_agendamento_diario[top_agendamento_diario["VALOR DIARIO"] == menor_valor_ag][["NOME", "IMPRODUTIVAS TOTAL", "VALOR DIARIO"]]
    menor_acumulado_ag = menores_acumulado_ag["IMPRODUTIVAS TOTAL"].min()
    top_dia_ag = top_agendamento_diario[top_agendamento_diario["IMPRODUTIVAS TOTAL"] == menor_acumulado_ag][["NOME", "IMPRODUTIVAS TOTAL", "VALOR DIARIO"]].iloc[0]


    rk = st.checkbox("Visualizar Ranking")
    if rk:
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
               
            }
            .card {
                padding: 20px;
                border-radius: 20px;
                text-align: center;
                box-shadow: 0 4px 12px rgba(100,100,100,0.2);
                transition: 0.3s;
                margin-bottom: 100px;
                animation: float 2.5s ease-in-out infinite;
                background-color: rgba(255, 255, 255, 0.05);
                border:1px solid rgba(255,255,255,0.2);
            }
        
            .card img {
                width: 100px;
                height: 100px;
                border-radius: 50%;  /* deixa redonda */
                object-fit: cover;   /* corta o excesso sem distorcer */
                margin-bottom: 12px;
                margin: 12px 10px;
            }
            .title {
                font-size: 18px;
                font-weight: 600;
                margin-bottom: 8px;
                color: white1;
            }
            .value {
                font-size: 19px;
                font-weight: 500;
                color: #00ffb3;
            }
            #improdutivas-diarias {
                font-size: 25px;
                margin-bottom: 30px;
            }
            
            </style>
            """,
            unsafe_allow_html=True
        )
        
        
        img_dia_cont = f'assets/imgs/{top_dia_cont['NOME']}.jpeg'   
        img_acum_cont =  f'assets/imgs/{top_controlador_mes['TOP MES'].iloc[0]}.jpeg'

        img_dia_ag = f'assets/imgs/{top_dia_ag['NOME']}.jpeg'   
        img_acum_ag =  f'assets/imgs/{top_agendamento_mes['TOP MES'].iloc[0]}.jpeg'
      

        def get_base64_of_image(image_path):
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()

        img_cont_dia = get_base64_of_image(img_dia_cont)
        img_cont_acum = get_base64_of_image(img_acum_cont)

        img_ag_dia = get_base64_of_image(img_dia_ag)
        img_ag_acum = get_base64_of_image(img_acum_ag)

        data_de_atualizacao = df["DATA"].iloc[0]        

       
        st.markdown(
            f"""
            <h2 class="data">Data de Atualização: {data_de_atualizacao}</h2>
            <div class="center-container">
                <div class="card">
                    <h4>🎖️ Top Controlador da semana</h4>
                    <img class="img-dia" src="data:image/jpeg;base64,{img_cont_dia}" width="120">
                    <div class="title">{top_dia_cont['NOME']}</div>
                    <div class="value">{top_dia_cont['VALOR DIARIO']} - IMPRODUTIVAS REPETIDAS</div>
                </div>
                <div class="card">
                    <h4>🏅 Top Controlador do Período</h4>
                    <img class="img-dia" src="data:image/jpeg;base64,{img_cont_acum}" width="120">
                    <div class="title">{top_controlador_mes['TOP MES'].iloc[0]}</div>
                    <div class="value">{int(top_controlador_mes['TOTAL MES'].iloc[0])} - IMPRODUTIVAS REPETIDAS</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


        if len(menores_cont) > 1:

            st.markdown(
                "<h2 style='font-size:30px;' >Acumulado dos melhores da Semana</h2>",
                unsafe_allow_html=True
            ) 


            fig_top_acumulado = px.bar(menores_acumulado_cont, x="NOME", y="IMPRODUTIVAS TOTAL", text="IMPRODUTIVAS TOTAL",)
            fig_top_acumulado.update_traces(
                    textposition="outside",  # ou "top center"
                    textfont=dict(size=14),
                )
            fig_top_acumulado.update_layout(
                    autosize = True,
                    width=None,
                    template="ggplot2",
                    uniformtext_minsize=8,
                    uniformtext_mode="hide",
                    margin=dict(t=30, b=0)
                )

            st.plotly_chart(fig_top_acumulado, use_container_width=True)

        st.markdown(
                "<h2 style='font-size:30px;' >Maiores improdutiva acumulado</h2>",
                unsafe_allow_html=True
        ) 

        fig_rank1 = px.bar(df, x="MAIOR IMPRODUTIVA", y="TOTAL IMPRODUTIVAS", color="TIPO IMPRO", text="TOTAL IMPRODUTIVAS")
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

        st.plotly_chart(fig_rank1, use_container_width=True)

    graficos = [
        "IMPRODUTIVAS TOTAL",
        "IMPRODUTIVAS ADESÃO",
        "IMPRODUTIVAS REPARO",
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

    
    va = st.checkbox("Visualizar Valores Gerais")

    if va:

        st.title("Valores Gerais")

        st.markdown(
                "<h2 style='font-size:30px;' >Improdutivas diarias</h2>",
                unsafe_allow_html=True
            ) 

        fig_diario = px.bar(top_controlador_diario, x="NOME", y="VALOR SEMANAL", text="VALOR SEMANAL",)
        fig_diario.update_traces(
                    textposition="outside",  # ou "top center"
                    textfont=dict(size=14),
                )
        
        fig_diario.update_layout(
                    autosize = True,
                    width=None,
                    template="ggplot2",
                    uniformtext_minsize=8,
                    uniformtext_mode="hide",
                    margin=dict(t=30, b=0)
                )

        st.plotly_chart(fig_diario, use_container_width=True)
        

        st.markdown(
            "<h2 style='font-size:30px;' >Valores acumuladas</h2>",
            unsafe_allow_html=True
        ) 
        if servico_escolhido == servs[0]:
            for i in graficos[:1]:
                gera_grafico(i)
        if servico_escolhido == servs[1]:
            for i in graficos[1:2]:
                gera_grafico(i)
        if servico_escolhido == servs[2]:
            for i in graficos[2:3]:
                gera_grafico(i)
        if servico_escolhido == servs[3]:
            for i in graficos[3:4]:
                gera_grafico(i)
    


            

elif authentication_status is False:
    st.error("Usuário ou senha incorreta")
elif authentication_status is None:
    st.info("Faça login")



