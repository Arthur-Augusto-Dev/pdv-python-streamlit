def gerar_comprovante(venda_id, data, itens, total, pagamento):
    largura = 34
    linhas = []
    linhas.append("=" * largura)
    linhas.append("      COMPROVANTE DE VENDA      ".center(largura))
    linhas.append("=" * largura)
    linhas.append(f"Venda n: {str(venda_id).ljust(largura-9)}")
    linhas.append(f"Data: {data}")
    linhas.append("-" * largura)
    linhas.append("Item          Qtd   V.Un   Sub")
    
    for item in itens:
        nome = item['nome'][:12].ljust(12)
        qtd = str(item['qtd']).center(5)
        preco = f"{item['preco']:.2f}".center(6)
        subtotal = f"{(item['qtd'] * item['preco']):.2f}".rjust(7)
        linhas.append(f"{nome} {qtd} {preco} {subtotal}")
        
    linhas.append("-" * largura)
    linhas.append(f"TOTAL:".ljust(largura-10) + f"R$ {total:>7.2f}")
    linhas.append(f"PAGAMENTO: {pagamento.upper()}")
    linhas.append("=" * largura)
    linhas.append("   Obrigado pela preferência!   ".center(largura))
    linhas.append("=" * largura)
    
    return "\n".join(linhas)