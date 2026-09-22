import csv
import random
from datetime import datetime, timedelta

# 1. Definindo o nosso cardápio
menu = [
    {"nome": "Prato Executivo Frango", "categoria": "Almoço", "preco": 25.00},
    {"nome": "Feijoada", "categoria": "Almoço", "preco": 35.00},
    {"nome": "Hambúrguer Artesanal", "categoria": "Lanches", "preco": 30.00},
    {"nome": "Pizza Margherita", "categoria": "Jantar", "preco": 45.00},
    {"nome": "Cerveja IPA", "categoria": "Bebidas", "preco": 15.00},
    {"nome": "Suco de Laranja", "categoria": "Bebidas", "preco": 8.00},
]

def gerar_vendas(num_vendas):
    vendas = []
    
    # Define a data de início: 90 dias atrás a partir de hoje
    data_inicio = datetime.now() - timedelta(days=90)

    for i in range(1, num_vendas + 1):
        # Gera uma data e hora aleatória dentro dos últimos 90 dias
        minutos_aleatorios = random.randint(0, 90 * 24 * 60)
        data_venda = data_inicio + timedelta(minutes=minutos_aleatorios)
        hora = data_venda.hour

        # 2. Lógica de Negócios: Pesos diferentes dependendo da hora do dia
        if 11 <= hora <= 14:
            # Horário de almoço
            opcoes = [item for item in menu if item["categoria"] in ["Almoço", "Bebidas"]]
        elif 18 <= hora <= 23:
            # Horário de jantar
            opcoes = [item for item in menu if item["categoria"] in ["Jantar", "Lanches", "Bebidas"]]
        else:
            # Outros horários (madrugada/manhã) - volume baixo, cardápio geral
            opcoes = menu

        # Escolhe um item baseado nas opções disponíveis para aquele horário
        item_vendido = random.choice(opcoes)
        
        # Simula a quantidade de itens comprados no mesmo pedido (de 1 a 3)
        quantidade = random.choices([1, 2, 3], weights=[70, 20, 10])[0]

        vendas.append({
            "id_venda": i,
            "data_hora": data_venda.strftime("%Y-%m-%d %H:%M:%S"),
            "prato": item_vendido["nome"],
            "categoria": item_vendido["categoria"],
            "quantidade": quantidade,
            "valor_total": round(item_vendido["preco"] * quantidade, 2)
        })

    return vendas

# 3. Executando a função e salvando em um arquivo
print("Gerando dados...")
dados_vendas = gerar_vendas(5000)

colunas = ["id_venda", "data_hora", "prato", "categoria", "quantidade", "valor_total"]

with open("vendas_restaurante.csv", mode="w", newline="", encoding="utf-8") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=colunas)
    escritor.writeheader()
    escritor.writerows(dados_vendas)

print("Arquivo 'vendas_restaurante.csv' gerado com sucesso com 5000 registros!")