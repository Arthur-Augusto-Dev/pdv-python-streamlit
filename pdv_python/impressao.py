from datetime import datetime

def gerar_cupom(venda_id, itens, total, pagamento):
    """
    itens = lista de tuplas:
    (produto, qtd, preco, total_item)
    """

    linhas = []
    linhas.append("========== CUPOM FISCAL ==========")
    linhas.append("        PDV - Sistema Python      ")
    linhas.append("----------------------------------")
    linhas.append(f"Venda Nº: {venda_id}")
    linhas.append(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    linhas.append("----------------------------------")

    for produto, qtd, preco, total_item in itens:
        linhas.append(
            f"{produto[:20]:20} {qtd:>3} x {preco:>6.2f} = {total_item:>7.2f}"
        )

    linhas.append("----------------------------------")
    linhas.append(f"TOTAL: R$ {total:.2f}")
    linhas.append(f"Pagamento: {pagamento}")
    linhas.append("----------------------------------")
    linhas.append("      Obrigado pela preferência   ")
    linhas.append("==================================")

    return "\n".join(linhas)
