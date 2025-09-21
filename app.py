import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from Utils.relatorio import gerar_pdf
from Utils.zipador import zipar_projeto
st.markdown("""
    <div style='background-color:#f0f0f0; padding:10px; border-radius:5px; text-align:center'>
        <h3 style='color:#333333;'>👷 Engenheiro Marcio Alves de Melo</h3>
    </div>
""", unsafe_allow_html=True)

# Caminho do arquivo
caminho_arquivo = "data/dados_obras.xlsx"

# Carrega os dados existentes ou cria novo
if os.path.exists(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo)
else:
    df = pd.DataFrame(columns=["Nome da Obra", "Tipo de Bebida", "Localização", "% Concluído", "Custo Previsto", "Custo Real"])
st.sidebar.header("🔍 Filtros")

obras_disponiveis = df["Nome da Obra"].unique()
tipos_disponiveis = df["Tipo de Bebida"].unique()

obra_selecionada = st.sidebar.selectbox("Filtrar por obra", options=["Todas"] + list(obras_disponiveis))
tipo_selecionado = st.sidebar.selectbox("Filtrar por tipo de bebida", options=["Todos"] + list(tipos_disponiveis))

# Aplica os filtros
df_filtrado = df.copy()
if obra_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["Nome da Obra"] == obra_selecionada]
if tipo_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Tipo de Bebida"] == tipo_selecionado]

# ---------- FORMULÁRIO ----------
st.header("📋 Cadastro ou Atualização de Obras")

with st.form("formulario_obra"):
    nome = st.text_input("Nome da Obra")
    bebida = st.selectbox("Tipo de Bebida", ["Cerveja", "Refrigerante", "Água Mineral", "Energético", "Vinho"])
    local = st.text_input("Localização")
    concluido = st.slider("% Concluído", 0, 100, 0)
    previsto = st.number_input("Custo Previsto (R$)", min_value=0.0, step=1000.0)
    real = st.number_input("Custo Real (R$)", min_value=0.0, step=1000.0)
    salvar = st.form_submit_button("💾 Salvar dados")

if salvar:
    nova_linha = {
        "Nome da Obra": nome,
        "Tipo de Bebida": bebida,
        "Localização": local,
        "% Concluído": concluido,
        "Custo Previsto": previsto,
        "Custo Real": real
    }
    df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
    df.to_excel(caminho_arquivo, index=False)
    st.success(f"Dados da obra '{nome}' salvos com sucesso!")

st.header("🏗️ Atualizar Progresso por Fase")

with st.form("formulario_fases"):
    obra_fases = st.selectbox("Selecione a obra", df["Nome da Obra"].unique())
    fase_atual = st.selectbox("Fase atual", ["Fundação", "Estrutura", "Acabamento", "Instalações"])
    fundacao = st.slider("Fundação (%)", 0, 100, 0)
    estrutura = st.slider("Estrutura (%)", 0, 100, 0)
    acabamento = st.slider("Acabamento (%)", 0, 100, 0)
    instalacoes = st.slider("Instalações (%)", 0, 100, 0)
    salvar_fases = st.form_submit_button("💾 Salvar Fases")

if salvar_fases:
    df.loc[df["Nome da Obra"] == obra_fases, "Fase Atual"] = fase_atual
    df.loc[df["Nome da Obra"] == obra_fases, "Fundação"] = fundacao
    df.loc[df["Nome da Obra"] == obra_fases, "Estrutura"] = estrutura
    df.loc[df["Nome da Obra"] == obra_fases, "Acabamento"] = acabamento
    df.loc[df["Nome da Obra"] == obra_fases, "Instalações"] = instalacoes
    df.to_excel(caminho_arquivo, index=False)
    st.success(f"Fases da obra '{obra_fases}' atualizadas com sucesso!")
st.header("📌 Progresso por Fase das Obras")

fases = ["Fundação", "Estrutura", "Acabamento", "Instalações"]

for _, linha in df_filtrado.iterrows():
    st.subheader(f"🏗️ {linha['Nome da Obra']} — Fase atual: {linha.get('Fase Atual', 'Não definida')}")
    for fase in fases:
        progresso = linha.get(fase, 0)
        st.progress(progresso / 100, text=f"{fase}: {progresso}%")
        if progresso < 50:
            st.warning(f"⚠️ Fase '{fase}' está atrasada ({progresso}%)")

# Corrige as colunas para garantir que sejam numéricas
df["% Concluído"] = pd.to_numeric(df["% Concluído"], errors="coerce").fillna(0)
df["Custo Previsto"] = pd.to_numeric(df["Custo Previsto"], errors="coerce").fillna(0)
df["Custo Real"] = pd.to_numeric(df["Custo Real"], errors="coerce").fillna(0)
# ---------- GRÁFICOS ----------
st.header("📊 Visualização dos Dados")

# Corrige as colunas para garantir que sejam numéricas
df["% Concluído"] = pd.to_numeric(df["% Concluído"], errors="coerce").fillna(0)
df["Custo Previsto"] = pd.to_numeric(df["Custo Previsto"], errors="coerce").fillna(0)
df["Custo Real"] = pd.to_numeric(df["Custo Real"], errors="coerce").fillna(0)

if not df.empty:
    fig1, ax1 = plt.subplots()
    df.plot(kind='bar', x='Nome da Obra', y='% Concluído', ax=ax1, color='skyblue')
    ax1.set_title("Andamento das Obras")
    ax1.set_ylabel("Percentual Concluído (%)")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    df.plot(kind='bar', x='Nome da Obra', y=['Custo Previsto', 'Custo Real'], ax=ax2)
    ax2.set_title("Comparativo de Custos por Obra")
    ax2.set_ylabel("Valor (R$)")
    st.pyplot(fig2)
else:
    st.warning("Nenhuma obra cadastrada ainda. Cadastre uma obra para visualizar os gráficos.")
st.header("📷 Fotos do Andamento das Obras")

for nome_obra in df["Nome da Obra"].unique():
    caminho_imagem = f"fotos_obras/{nome_obra}.jpg"
    if os.path.exists(caminho_imagem):
        st.subheader(f"📍 {nome_obra}")
        st.image(caminho_imagem, caption=f"Andamento da obra: {nome_obra}", use_column_width=True)
    else:
        st.info(f"Sem imagem disponível para a obra: {nome_obra}")
st.header("🚨 Impacto na Produção")

for _, linha in df.iterrows():
    impacto = []
    if linha["% Concluído"] < 50:
        impacto.append("⚠️ Obra atrasada")
    if linha["Custo Real"] > linha["Custo Previsto"]:
        impacto.append("💸 Custo acima do previsto")
    if not impacto:
        impacto.append("✅ Sem impacto relevante")

    st.markdown(f"**{linha['Nome da Obra']}** — {' | '.join(impacto)}")