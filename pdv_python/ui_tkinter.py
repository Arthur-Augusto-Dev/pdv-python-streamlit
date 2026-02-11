import tkinter as tk
from tkinter import messagebox
from database import conectar, criar_tabelas

# garante que o banco exista
criar_tabelas()

# =========================
# VARIÁVEIS DE CONTROLE
# =========================
carrinho = []

# =========================
# FUNÇÕES
# =========================
def nova_venda():
    global carrinho
    carrinho = []
    txt_cupom.delete("1.0", tk.END)
    lbl_status.config(text="Nova venda iniciada")

def adicionar():
    produto = entry_produto.get()
    qtd = entry_qtd.get()

    if not produto or not qtd:
        lbl_status.config(text="Preencha produto e quantidade")
        return

    try:
        qtd = int(qtd)
    except ValueError:
        lbl_status.config(text="Quantidade inválida")
        return

    preco = 10.0  # valor fixo para teste
    total_item = qtd * preco

    carrinho.append((produto, qtd, preco, total_item))

    txt_cupom.insert(
        tk.END,
        f"Produto: {produto} | Qtd: {qtd} | R$ {total_item:.2f}\n"
    )

    entry_produto.delete(0, tk.END)
    entry_qtd.delete(0, tk.END)
    lbl_status.config(text="Item adicionado")

def finalizar():
    if not carrinho:
        messagebox.showwarning("Aviso", "Carrinho vazio")
        return

    total = sum(item[3] for item in carrinho)

    with conectar() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO vendas (total, pagamento) VALUES (?, ?)",
            (total, "Dinheiro")
        )
        venda_id = cur.lastrowid

        for item in carrinho:
            cur.execute(
                "INSERT INTO itens_venda (venda_id, produto, qtd, preco) VALUES (?, ?, ?, ?)",
                (venda_id, item[0], item[1], item[2])
            )

        conn.commit()

    txt_cupom.insert(tk.END, f"\nTOTAL: R$ {total:.2f}\n")
    lbl_status.config(text="Venda finalizada")
    carrinho.clear()

# =========================
# INTERFACE
# =========================
root = tk.Tk()
root.title("PDV - Caixa")
root.geometry("420x500")

tk.Button(root, text="Nova Venda", command=nova_venda).pack(pady=5)

tk.Label(root, text="Produto").pack()
entry_produto = tk.Entry(root)
entry_produto.pack()

tk.Label(root, text="Quantidade").pack()
entry_qtd = tk.Entry(root)
entry_qtd.pack()

tk.Button(root, text="Adicionar Item", command=adicionar).pack(pady=5)
tk.Button(root, text="Finalizar Venda", command=finalizar).pack(pady=5)

lbl_status = tk.Label(root, text="")
lbl_status.pack(pady=5)

txt_cupom = tk.Text(root, height=15, width=45)
txt_cupom.pack()

root.mainloop()
