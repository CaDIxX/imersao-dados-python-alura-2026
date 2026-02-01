import pandas as pd
import plotly.express as px
import streamlit as st
import pycountry

st.set_page_config(
    page_title='Dashboards de Análise de salários na Área de Dados',
    page_icon='📊',
    layout="wide"
)

df = (
    pd.read_csv(r"https://raw.githubusercontent.com/guilhermeonrails/data-jobs/refs/heads/main/salaries.csv",
                sep=',',
                encoding='latin1',
                engine='python')
    )


df['work_year'] = df['work_year'].astype('Int64')

column_translations = {
    'work_year': 'ano',
    'experience_level': 'nivel_experiencia',
    'employment_type': 'tipo_emprego',
    'job_title': 'cargo',
    'salary': 'salario',
    'salary_currency': 'moeda',
    'salary_in_usd': 'usd',
    'employee_residence': 'residencia',
    'remote_ratio': 'remoto',
    'company_location': 'empresa',
    'company_size': 'porte_empresa'
}
df = df.rename(columns=column_translations)


# Criando os Filtros
st.sidebar.header('Filtros')

anos_disponiveis = sorted(df['ano'].dropna().unique()) # tirei os valores nulos
anos_selecionados = st.sidebar.multiselect('Ano', anos_disponiveis, default=anos_disponiveis)


senioridade_traduzida = {
    'EN': 'Júnior',
    'EX': 'Executivo',
    'MI': 'Pleno',
    'SE': 'Senior'
}
df['nivel_experiencia'] = df['nivel_experiencia'].map(senioridade_traduzida)
senioridade_disponiveis = sorted(df['nivel_experiencia'].unique())
senioridade_selecionadas = st.sidebar.multiselect('Senioridade', senioridade_disponiveis, default=senioridade_disponiveis)


contrato_traduzido = {
    'FT': 'Tempo Integral',
    'PT': 'Tempo Parcial',
    'FL':  'Freelance',
    'CT': 'Contrato'
}
df['tipo_emprego'] = df['tipo_emprego'].map(contrato_traduzido)
contratos_disponiveis = sorted(df['tipo_emprego'].unique())
contratos_selecionados = st.sidebar.multiselect('Contrato', contratos_disponiveis, default=contratos_disponiveis)

porte_empresa_traduzido = {
    'L': 'Grande',
    'M': 'Médio',
    'S': 'Pequeno'
}
df['porte_empresa'] = df['porte_empresa'].map(porte_empresa_traduzido)
tamanhos_disponiveis = sorted(df['porte_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect('Porte da Empresa', tamanhos_disponiveis, default=tamanhos_disponiveis)

# O dataframe principal é filtrado com base nas seleções feitas na barra lateral
df_filtrado =df[
    (df['ano'].isin(anos_selecionados)) &
    (df['nivel_experiencia'].isin(senioridade_selecionadas)) &
    (df['tipo_emprego'].isin(contratos_selecionados)) &
    (df['porte_empresa'].isin(tamanhos_selecionados))
]

st.title("Dashboard de Análise de Salários na Área de Dados")
st.markdown("Exprore os dados salariais na área de dados no ùltimos anos. Utilize os filtros à esquerda para fazer sua análise")


# Métricas Principais
st.subheader("Métricas gerais (Salário Anual em USD)")

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    salario_minimo = df_filtrado['usd'].min()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]

else:
    salario_medio, salario_maximo, salario_minimo, total_registros, cargo_mais_frequente = 0, 0, 0, 0, ""

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Salário Médio", f"${salario_medio:.2f}")
col2.metric("Salário Maximo", f"${salario_maximo:.2f}")
col3.metric("Salário Minimo", f"${salario_minimo:.2f}")
col4.metric("Total de Funcionários", f"{total_registros}")
col5.metric("Cargo Mais Frequênte", f"{cargo_mais_frequente.capitalize()}")

st.markdown("---")

# Análise Visuais com Plotly
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = (df_filtrado.groupby('cargo')['usd']
                      .mean()
                      .nlargest(10)
                      .sort_values(ascending=False)
                      .reset_index())
        
        graficos_cargos = px.bar(
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h',
            title="Top 10 cargos por salário médio",
            labels={
                'usd': 'Média salarial anual (USD)',
                'cargo': ''
            }
        )
        graficos_cargos.update_layout(title_x=0.1, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(graficos_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")
    

with col_graf2:
    if not df_filtrado.empty:
        graficos_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title='Distibuição de salários anuais',
            labels={
                'usd': 'Faixa Salarial(USD)',
                'count': ''
            }
        )
        graficos_hist.update_layout(title_x=0.1)
        st.plotly_chart(graficos_hist, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir no gráfico de distribuição.')


col_graf3, col_graf4 = st.columns(2)

df_filtrado['remoto'] = df_filtrado['remoto'].astype('str')
substituir_regime_empregaticio = {
    '0': 'Presencial',
    '50': 'Hibrido',
    '100': 'Remoto'
}
df_filtrado['remoto'] = df_filtrado['remoto'].map(substituir_regime_empregaticio)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['regime empregatício', 'quantidades']
        graficos_remoto = px.pie(
            remoto_contagem,
            names=remoto_contagem.columns[0],
            values=remoto_contagem.columns[1],
            title='Proporção dos Regime Empregatício',
            hole=0.5
        )
        graficos_remoto.update_traces(textinfo='percent+label')
        graficos_remoto.update_layout(title_x=0.1)
        st.plotly_chart(graficos_remoto, use_container_width=True)
    else:
        st.warning('Nenhum dado para exibir no gráfico dos tipos de trabalho.')

def iso2_to_iso3(code):
    try:
        return pycountry.countries.get(alpha_2=code).alpha_3
    except:
        return None

with col_graf4:
    if not df_filtrado.empty:
        filtro = (df_filtrado['cargo']
          .str
          .contains('Data Scientist', 
                    case=False, 
                    na=False)
          )
        df_ds = df_filtrado.loc[filtro].copy()

        if not df_ds.empty:
            df_ds['residencia_iso3'] = df_ds['residencia'].apply(iso2_to_iso3)
        
            media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
            graficos_paises = px.choropleth(
                media_ds_pais,
                locations='residencia_iso3',
                color='usd',
                color_continuous_scale='rdylgn',
                title='Salário médio de Cientista de Dados por país',
                labels={
                    'usd': 'Salário Médio (USD)',
                    'residencia_iso3': 'País'
                }
            )
            graficos_paises.update_layout(title_x=0.1)
            st.plotly_chart(graficos_paises, use_container_width=True)
        else:
            st.warning("Nenhum 'Data Scientist' encontrado nos filtros selecionados.")
    else:
        st.warning('Nenhum dado para exibir no gráfico de países.')

st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)