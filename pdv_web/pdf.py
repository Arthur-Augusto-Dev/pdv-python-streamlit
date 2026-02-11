from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet

def gerar_pdf(itens, total, pagamento, arquivo="cupom.pdf"):

    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("CUPOM FISCAL - PDV", styles["Heading1"]))
    elementos.append(Spacer(1, 20))

    for item in itens:
        texto = f"{item['nome']} x{item['qtd']} - R$ {item['preco']:.2f}"
        elementos.append(Paragraph(texto, styles["Normal"]))

    elementos.append(Spacer(1, 20))
    elementos.append(Paragraph(f"TOTAL: R$ {total:.2f}", styles["Heading2"]))
    elementos.append(Paragraph(f"Pagamento: {pagamento}", styles["Normal"]))


    doc = SimpleDocTemplate(arquivo)
    doc.build(elementos)

    return arquivo