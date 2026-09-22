import sqlite3
import csv

conexao = sqlite3.connect("restaurante.db")
cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS vendas (
    id_venda INTEGER PRIMARY KEY,
    data_hora TEXT,
    prato TEXT,
    categoria TEXT,
    quantidade INTEGER,
    valor_total REAL
)
''')

cursor.execute('DELETE FROM vendas')

print("Lendo arquivo csv...")
with open("vendas_restaurante.csv", "r", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo)

    dados = [(
        linha["id_venda"],
        linha["data_hora"],
        linha["prato"],
        linha["categoria"],
        linha["quantidade"],
        linha["valor_total"],
    ) for linha in leitor]

cursor.executemany('''
INSERT INTO vendas (id_venda, data_hora, prato, categoria, quantidade, valor_total)
VALUES (?, ?, ?, ?, ?, ?)
''', dados)

conexao.commit()
print("Sucesso! 5000 registros inseridos no banco 'restaurant.db'.")

print("\n=== TOP 3 PRATOS MAIS LUCRATIVOS ===")

cursor.execute('''
SELECT prato, SUM(valor_total) as receita_total
FROM vendas
GROUP BY prato
ORDER by receita_total DESC
LIMIT 3
''')

resultados = cursor.fetchall()
for linha in resultados:
    nome_prato = linha[0]
    receita = linha[1]
    print(f"Prato: {nome_prato} | Receita Total: R$ {receita:.2f}")

conexao.close()