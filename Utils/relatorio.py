from fpdf import FPDF

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Relatório da Obra", ln=True, align="C")
    pdf.ln(10)

    for chave, valor in dados.items():
        pdf.cell(200, 10, txt=f"{chave}: {valor}", ln=True)

    pdf.output("relatorio_obra.pdf")