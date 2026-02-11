def gerar_comprovante(venda_id, data, itens, total, pagamento):
    linhas = []
    linhas.append("====== COMPROVANTE DE VENDA ======")
    linhas.append(f"Venda nº: {venda_id}")
    linhas.append(f"Data: {data}")
    linhas.append("---------------------------------")

    for item in itens:
        linhas.append(
            f"{item['nome']}  x{item['qtd']}  "
            f"R$ {item['preco']:.2f}"
        )

    linhas.append("---------------------------------")
    linhas.append(f"TOTAL: R$ {total:.2f}")
    linhas.append(f"Pagamento: {pagamento}")
    linhas.append("=================================")

    return "\n".join(linhas)