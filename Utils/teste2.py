import matplotlib.pyplot as plt

def grafico_andamento(df):
    fig, ax = plt.subplots()
    etapas = df["Etapa"]
    andamento = df["% Concluído"]

    ax.bar(etapas, andamento, color="skyblue")
    ax.set_title("Andamento Físico por Etapa")
    ax.set_ylabel("% Concluído")
    ax.set_xticklabels(etapas, rotation=45, ha="right")

    return fig

def grafico_custos(df):
    fig, ax = plt.subplots()
    etapas = df["Etapa"]
    previsto = df["Custo Previsto"]
    real = df["Custo Real"]

    largura = 0.35
    x = range(len(etapas))

    ax.bar(x, previsto, width=largura, label="Previsto", color="orange")
    ax.bar([i + largura for i in x], real, width=largura, label="Real", color="green")

    ax.set_title("Custo Previsto vs. Real por Etapa")
    ax.set_ylabel("R$ (mil)")
    ax.set_xticks([i + largura / 2 for i in x])
    ax.set_xticklabels(etapas, rotation=45, ha="right")
    ax.legend()

    return fig