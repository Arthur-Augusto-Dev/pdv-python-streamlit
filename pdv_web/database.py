import sqlite3

def conectar():
    return sqlite3.connect("pdv.db", check_same_thread=False)


def criar_tabelas():
    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS produtos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        preco REAL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS vendas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        total REAL,
        pagamento TEXT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS itens_venda(
        venda_id INTEGER,
        produto TEXT,
        qtd INTEGER,
        preco REAL
    )
    """)

    conn.commit()
    conn.close()