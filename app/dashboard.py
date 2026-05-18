import os
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Mercado global de videogames", layout="wide")

# 2. Ingestão de Dados
@st.cache_data
def carregar_dados():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_csv = os.path.join(diretorio_atual, '..', 'data', 'base_tratada.csv')
    
    df = pd.read_csv(caminho_csv)
    df['release_date'] = pd.to_datetime(df['release_date'])
    df['ano'] = df['release_date'].dt.year
    return df

df_original = carregar_dados()
df_original = df_original[df_original['ano'] >= 1980]

# 3. Barra Lateral (Filtros Interativos)
# SVG da barra lateral
st.sidebar.markdown(
    """
    <div style="margin-bottom: 15px;">
        <svg width="50" height="50" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
            <g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
            <g id="SVGRepo_iconCarrier"> 
                <path fill-rule="evenodd" clip-rule="evenodd" d="M10.6669 6.13443L10.165 5.77922C9.44862 5.27225 8.59264 5 7.71504 5H7.10257C6.69838 5 6.29009 5.02549 5.90915 5.16059C3.52645 6.00566 1.88749 9.09504 2.00604 16.1026C2.02992 17.5145 2.3603 19.075 3.63423 19.6842C4.03121 19.8741 4.49667 20 5.02671 20C5.66273 20 6.1678 19.8187 6.55763 19.5632C6.96641 19.2953 7.32633 18.9471 7.68612 18.599C8.13071 18.1688 8.57511 17.7389 9.11125 17.4609C9.69519 17.1581 10.3434 17 11.0011 17H12.9989C13.6566 17 14.3048 17.1581 14.8888 17.4609C15.4249 17.7389 15.8693 18.1688 16.3139 18.599C16.6737 18.9471 17.0336 19.2953 17.4424 19.5632C17.8322 19.8187 18.3373 20 18.9733 20C19.5033 20 19.9688 19.8741 20.3658 19.6842C21.6397 19.075 21.9701 17.5145 21.994 16.1026C22.1125 9.09503 20.4735 6.00566 18.0908 5.16059C17.7099 5.02549 17.3016 5 16.8974 5H16.2849C15.4074 5 14.5514 5.27225 13.8351 5.77922L13.3332 6.13441C12.9434 6.41029 12.4776 6.55844 12 6.55844C11.5225 6.55844 11.0567 6.41029 10.6669 6.13443ZM16.75 9C17.1642 9 17.5 9.33579 17.5 9.75C17.5 10.1642 17.1642 10.5 16.75 10.5C16.3358 10.5 16 10.1642 16 9.75C16 9.33579 16.3358 9 16.75 9ZM7.5 9.25C7.91421 9.25 8.25 9.58579 8.25 10V10.75H9C9.41421 10.75 9.75 11.0858 9.75 11.5C9.75 11.9142 9.41421 12.25 9 12.25H8.25V13C8.25 13.4142 7.91421 13.75 7.5 13.75C7.08579 13.75 6.75 13.4142 6.75 13V12.25H6C5.58579 12.25 5.25 11.9142 5.25 11.5C5.25 11.0858 5.58579 10.75 6 10.75H6.75V10C6.75 9.58579 7.08579 9.25 7.5 9.25ZM19 11.25C19 11.6642 18.6642 12 18.25 12C17.8358 12 17.5 11.6642 17.5 11.25C17.5 10.8358 17.8358 10.5 18.25 10.5C18.6642 10.5 19 10.8358 19 11.25ZM15.25 12C15.6642 12 16 11.6642 16 11.25C16 10.8358 15.6642 10.5 15.25 10.5C14.8358 10.5 14.5 10.8358 14.5 11.25C14.5 11.6642 14.8358 12 15.25 12ZM17.5 12.75C17.5 12.3358 17.1642 12 16.75 12C16.3358 12 16 12.3358 16 12.75C16 13.1642 16.3358 13.5 16.75 13.5C17.1642 13.5 17.5 13.1642 17.5 12.75Z" fill="#ffffff"></path> 
            </g>
        </svg>
    </div>
    """, 
    unsafe_allow_html=True
)
st.sidebar.header("Filtros Interativos")

# Filtro de Região
regiao_opcoes = {
    'Global': 'total_sales',
    'América do Norte': 'na_sales',
    'Japão': 'jp_sales',
    'Europa/África (PAL)': 'pal_sales',
    'Outros': 'other_sales'
}
regiao_selecionada = st.sidebar.selectbox("Região de Análise", list(regiao_opcoes.keys()))
col_vendas = regiao_opcoes[regiao_selecionada]

# Filtro de Período
ano_min = int(df_original['ano'].min())
ano_max = int(df_original['ano'].max())
ano_selecionado = st.sidebar.slider("Período de Lançamento", ano_min, ano_max, (ano_min, ano_max))

# Filtros categóricos
generos_selecionados = st.sidebar.multiselect("Gênero", options=df_original['genre'].dropna().unique())
consoles_selecionados = st.sidebar.multiselect("Console", options=df_original['console'].dropna().unique())

st.sidebar.markdown("---")
ocultar_outliers = st.sidebar.checkbox("Ocultar Mega-Hits (Apenas Gráfico de Dispersão)", value=False)
st.sidebar.markdown("---")

vendas_min_ranking = st.sidebar.number_input(
    "Vendas mínimas (ranking de crítica) (Mi)", 
    min_value=0.0, 
    value=0.5, # Padrão inicial de 500 mil cópias
    step=0.1,
    help="Define a nota de corte para remover jogos com baixo volume de vendas do ranking de melhor avaliados."
)

# 4. Aplicação dos Filtros de Dados
df_filtrado = df_original[
    (df_original['ano'] >= ano_selecionado[0]) & 
    (df_original['ano'] <= ano_selecionado[1])
]

if generos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['genre'].isin(generos_selecionados)]

if consoles_selecionados:
    df_filtrado = df_filtrado[df_filtrado['console'].isin(consoles_selecionados)]

st.title("Análise do mercado global de videogames (1980-2024)")

# Evita quebra de layout caso o filtro retorne vazio
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

# --- SEÇÃO 1: VENDAS E FATURAMENTO ---
st.header("💰 Vendas e faturamento")
col1, col2, col3, col4 = st.columns(4)

vendas_totais = df_filtrado[col_vendas].sum()
media_vendas = df_filtrado[col_vendas].mean()
idx_max_vendas = df_filtrado[col_vendas].idxmax() if not df_filtrado[col_vendas].isnull().all() else None

with col1:
    with st.container(border=True):
        st.metric(f"Vendas totais ({regiao_selecionada})", f"{vendas_totais:.2f} Mi")

with col2:
    with st.container(border=True):
        st.metric("Média por jogo", f"{media_vendas:.2f} Mi")

with col3:
    with st.container(border=True):
        if idx_max_vendas is not None:
            st.metric("Recorde histórico de vendas", f"{df_filtrado.loc[idx_max_vendas, col_vendas]:.2f} Mi")
        else:
            st.metric("Recorde histórico", "N/A")

with col4:
    with st.container(border=True):
        if idx_max_vendas is not None:
            st.metric("Título mais vendido", df_filtrado.loc[idx_max_vendas, 'title'])
        else:
            st.metric("Título mais vendido", "N/A")


# --- SEÇÃO 2: RECEPÇÃO E CRÍTICA ---
st.header("⭐ Recepção e crítica")
col5, col6, col7, col8 = st.columns(4)

media_critica = df_filtrado['critic_score'].mean()
jogos_aclamados = df_filtrado[df_filtrado['critic_score'] > 9.0]
fracassos = df_filtrado[df_filtrado['critic_score'] < 4.0]
idx_max_critica = df_filtrado['critic_score'].dropna().idxmax() if not df_filtrado['critic_score'].dropna().empty else None

with col5:
    with st.container(border=True):
        st.metric("Média geral da crítica", f"{media_critica:.1f}/10" if pd.notnull(media_critica) else "N/A")

with col6:
    with st.container(border=True):
        st.metric("Total de jogos aclamados (>9)", len(jogos_aclamados))

with col7:
    with st.container(border=True):
        st.metric("Total de fracassos (<4)", len(fracassos))

with col8:
    with st.container(border=True):
        if idx_max_critica is not None:
            st.metric("Título mais aclamado", df_filtrado.loc[idx_max_critica, 'title'])
        else:
            st.metric("Título mais aclamado", "N/A")

# --- SEÇÃO 3: INDÚSTRIA E MERCADO ---
st.header("🏭 Indústria e mercado")

# Linha 1: Volumetria geral
c1, c2, c3 = st.columns(3)

with c1:
    with st.container(border=True):
        st.metric("Total de jogos lançados", df_filtrado['title'].nunique())

with c2:
    with st.container(border=True):
        st.metric("Consoles ativos", df_filtrado['console'].nunique())

with c3:
    with st.container(border=True):
        st.metric("Total de publicadoras", df_filtrado['publisher'].nunique())

# Linha 2: Lideranças em Rentabilidade
c4, c5, c6 = st.columns(3)

with c4:
    with st.container(border=True):
        val_gen_rentavel = df_filtrado.groupby('genre')[col_vendas].sum().idxmax() if not df_filtrado.empty else "N/A"
        st.metric("Gênero mais rentável", val_gen_rentavel)

with c5:
    with st.container(border=True):
        val_pub_rentavel = df_filtrado.groupby('publisher')[col_vendas].sum().idxmax() if not df_filtrado.empty else "N/A"
        st.metric("Publicadora mais rentável", val_pub_rentavel)

with c6:
    with st.container(border=True):
        val_con_rentavel = df_filtrado.groupby('console')[col_vendas].sum().idxmax() if not df_filtrado.empty else "N/A"
        st.metric("Console mais rentável", val_con_rentavel)

# Linha 3: Lideranças em Aclamação da crítica
c7, c8, c9 = st.columns(3)

with c7:
    with st.container(border=True):
        val_pub_aclamada = jogos_aclamados['publisher'].mode()[0] if not jogos_aclamados.empty else "N/A"
        st.metric("Publicadora mais aclamada", val_pub_aclamada)

with c8:
    with st.container(border=True):
        val_gen_aclamado = jogos_aclamados['genre'].mode()[0] if not jogos_aclamados.empty else "N/A"
        st.metric("Gênero mais aclamado", val_gen_aclamado)

with c9:
    with st.container(border=True):
        val_con_aclamado = jogos_aclamados['console'].mode()[0] if not jogos_aclamados.empty else "N/A"
        st.metric("Console com mais títulos aclamados", val_con_aclamado)

st.markdown("---")

# --- GRÁFICOS: EVOLUÇÃO ---
st.header("Evolução histórica")
linha1_col1, linha1_col2 = st.columns(2)

with linha1_col1:
    vendas_ano = df_filtrado.groupby('ano')[col_vendas].sum().reset_index()
    fig_evolucao = px.line(vendas_ano, x='ano', y=col_vendas, title="Evolução geral de vendas", markers=True)
    st.plotly_chart(fig_evolucao, use_container_width=True)

with linha1_col2:
    vendas_console = df_filtrado.groupby(['ano', 'console'])[col_vendas].sum().reset_index()
    fig_ciclo = px.line(vendas_console, x='ano', y=col_vendas, color='console', title="Comparativo de ciclo de vida por console")
    st.plotly_chart(fig_ciclo, use_container_width=True)

# --- GRÁFICOS: TENDÊNCIAS E MARKET SHARE DE GÊNEROS ---
linha2_col1, linha2_col2 = st.columns(2)

with linha2_col1:
    vendas_genero_ano = df_filtrado.groupby(['ano', 'genre'])[col_vendas].sum().reset_index()
    fig_tendencias = px.line(vendas_genero_ano, x='ano', y=col_vendas, color='genre', title="Tendências de consumo por gênero")
    st.plotly_chart(fig_tendencias, use_container_width=True)

with linha2_col2:
    fig_pizza_gen = px.pie(df_filtrado, values=col_vendas, names='genre', title="Market share de gêneros", hole=0.4)
    st.plotly_chart(fig_pizza_gen, use_container_width=True)

st.markdown("---")

# --- GRÁFICOS: TOP 10 RANKINGS ---
st.header("Rankings comerciais")

# Linha 1: Jogos (Mais Vendidos e Melhor Avaliados)
linha1_col1, linha1_col2 = st.columns(2)

with linha1_col1:
    top_jogos_vendas = df_filtrado.groupby('title')[col_vendas].sum().nlargest(10).reset_index()
    fig_jogos_vendas = px.bar(top_jogos_vendas, x=col_vendas, y='title', orientation='h', title="Top 10 jogos mais vendidos")
    fig_jogos_vendas.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_jogos_vendas, use_container_width=True)

with linha1_col2:
    # Agrupa calculando a média da nota e a soma das vendas da região dinâmica
    top_jogos_critica = df_filtrado.groupby('title').agg(
        critic_score=('critic_score', 'mean'),
        vendas_regiao=(col_vendas, 'sum')
    ).reset_index()

    # Aplica a nota de corte baseada nas vendas mínimas definidas na barra lateral
    top_jogos_critica = top_jogos_critica[top_jogos_critica['vendas_regiao'] >= vendas_min_ranking]

    # Ordena por nota (decrescente) e usa as vendas como critério secundário de desempate
    top_jogos_critica = top_jogos_critica.sort_values(
        by=['critic_score', 'vendas_regiao'], 
        ascending=[False, False]
    ).head(10)

    # Renderização do gráfico de barras horizontais
    fig_jogos_critica = px.bar(
        top_jogos_critica, 
        x='critic_score', 
        y='title', 
        orientation='h', 
        title="Top 10 jogos melhor avaliados",
        labels={'critic_score': 'Nota da crítica', 'title': 'Título'},
        hover_data={'vendas_regiao': ':.2f'}
    )
    
    # Garante a exibição ordenada do maior para o menor de cima para baixo
    fig_jogos_critica.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_jogos_critica, use_container_width=True)

# Linha 2: Consoles e Gêneros
linha2_col1, linha2_col2 = st.columns(2)

with linha2_col1:
    top_console = df_filtrado.groupby('console')[col_vendas].sum().nlargest(10).reset_index()
    fig_console = px.bar(top_console, x=col_vendas, y='console', orientation='h', title="Top 10 consoles")
    fig_console.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_console, use_container_width=True)

with linha2_col2:
    top_gen = df_filtrado.groupby('genre')[col_vendas].sum().nlargest(10).reset_index()
    fig_gen = px.bar(top_gen, x=col_vendas, y='genre', orientation='h', title="Top 10 gêneros")
    fig_gen.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_gen, use_container_width=True)

# Linha 3: Publicadoras
linha3_col1, linha3_col2 = st.columns(2)

with linha3_col1:
    top_pub = df_filtrado.groupby('publisher')[col_vendas].sum().nlargest(10).reset_index()
    fig_pub = px.bar(top_pub, x=col_vendas, y='publisher', orientation='h', title="Top 10 publicadoras")
    fig_pub.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_pub, use_container_width=True)

st.markdown("---")

# --- GRÁFICOS: DISPERSÃO E DISTRIBUIÇÃO REGIONAL ---
col_disp, col_pizza_reg = st.columns([2, 1])

with col_disp:
    st.header("Relação crítica vs vendas")
    df_dispersao = df_filtrado.copy()
    
    if ocultar_outliers and not df_dispersao.empty:
        q1 = df_dispersao[col_vendas].quantile(0.25)
        q3 = df_dispersao[col_vendas].quantile(0.75)
        iqr = q3 - q1
        limite_sup = q3 + 1.5 * iqr
        df_dispersao = df_dispersao[df_dispersao[col_vendas] <= limite_sup]
    
    fig_scatter = px.scatter(
        df_dispersao, 
        x=col_vendas, 
        y='critic_score', 
        color='genre',
        hover_data=['title', 'console', 'genre'],
        title="Impacto da nota nas vendas"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_pizza_reg:
    st.header("Distribuição regional")
    if not df_filtrado.empty:
        vendas_regiao = pd.DataFrame({
            'Região': ['América do Norte', 'Japão', 'Europa/PAL', 'Outros'],
            'Vendas': [
                df_filtrado['na_sales'].sum(), 
                df_filtrado['jp_sales'].sum(), 
                df_filtrado['pal_sales'].sum(), 
                df_filtrado['other_sales'].sum()
            ]
        })
        fig_pizza_r = px.pie(vendas_regiao, values='Vendas', names='Região', hole=0.4)
        st.plotly_chart(fig_pizza_r, use_container_width=True)