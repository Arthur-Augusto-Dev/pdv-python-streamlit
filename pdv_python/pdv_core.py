from database import salvar_venda

def registrar_venda(itens, forma_pagamento):
    total_venda = 0
    for item in itens:
        total_venda += item["Preço Unit."] * item["Qtd"]
    
    total_venda = round(total_venda, 2)
    venda_id, data_hora = salvar_venda(total_venda, forma_pagamento)
    
    return venda_id, total_venda, data_hora