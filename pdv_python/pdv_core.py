from database import conectar
from datetime import datetime

def registrar_venda(itens, pagamento):
    with conectar() as conn:
        cur = conn.cursor()

        # cria venda
        cur.execute(
            "INSERT INTO vendas (total, pagamento) VALUES (?, ?)",
            (0, pagamento)
        )
        venda_id = cur.lastrowid

        total = 0

        for item in itens:
            subtotal = item["qtd"] * item["preco"]
            total += subtotal

            cur.execute("""
                INSERT INTO itens_venda (venda_id, produto, qtd, preco)
                VALUES (?, ?, ?, ?)
            """, (
                venda_id,
                item["nome"],
                item["qtd"],
                item["preco"]
            ))

            # fecha venda
        cur.execute(
            "UPDATE vendas SET total = ? WHERE id = ?",
            (total, venda_id)
        )

        conn.commit()

        return venda_id, total, datetime.now().strftime("%d/%m/%Y %H:%M")