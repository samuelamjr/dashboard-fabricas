import zipfile
import os

def zipar_projeto():
    with zipfile.ZipFile("projeto_dashboard_completo.zip", "w") as zipf:
        arquivos = [
            "relatorio_obra.pdf",
            "grafico_andamento.png",
            "grafico_custos.png"
        ]
        for arquivo in arquivos:
            if os.path.exists(arquivo):
                zipf.write(arquivo)