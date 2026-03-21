import sqlite3
from datetime import datetime

def criar_tabelas():
    conn = sqlite3.connect('pdv.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL,
            forma_pagamento TEXT,
            data_hora TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_venda(valor, forma_pgto):
    conn = sqlite3.connect('pdv.db')
    cursor = conn.cursor()
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cursor.execute('INSERT INTO vendas (valor, forma_pagamento, data_hora) VALUES (?, ?, ?)',
                   (valor, forma_pgto, data_hora))
    venda_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return venda_id, data_hora

def obter_vendas_do_dia():
    conn = sqlite3.connect('pdv.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vendas')
    dados = cursor.fetchall()
    conn.close()
    return dados
