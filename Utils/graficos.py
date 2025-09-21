import matplotlib.pyplot as plt

def grafico_andamento(df):
    fig, ax = plt.subplots()
    df.plot(kind='bar', x='Nome da Obra', y='% Concluído', ax=ax, color='skyblue')
    ax.set_title("Andamento das Obras")
    ax.set_ylabel("Percentual Concluído (%)")
    return fig

def grafico_custos(df):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    df.plot(kind='bar', x='Nome da Obra', y='Custo Real', ax=ax, color='orange')
    ax.set_title("Custo Real por Obra")
    ax.set_ylabel("Valor (R$)")
    return fig