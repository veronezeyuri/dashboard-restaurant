import sqlite3
import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

chave_cache = "dashboard:top_3_quantidades"

print("Tentando buscar no Cache (Redis)...")
inicio_tempo = time.time()

resultado_cache = r.get(chave_cache)

if resultado_cache:
    print("CACHE HIT - Dados encontrados no Redis na memória RAM.")
    dados = json.loads(resultado_cache)
else:
    print("CACHE MISS - Dados não estão no Redis. Indo buscar no SQLite...")

    conexao = sqlite3.connect("restaurante.db")
    cursor = conexao.cursor()

    cursor.execute('''
    SELECT prato, SUM(quantidade) as quantidade_total
    FROM vendas
    GROUP BY prato
    ORDER BY quantidade_total DESC
    LIMIT 3
    ''')

    dados = [{"prato": linha[0], "quantidade": linha[1]} for linha in cursor.fetchall()]
    conexao.close()

    r.setex(chave_cache, 60, json.dumps(dados))
    print("Resultado salvo no Redis! Nos próximos 60 segundos, a resposta será imediata.")

fim_tempo = time.time()

print("\n=== RESULTADO ===")
for item in dados:
    print(f"Prato: {item['prato']} | Unidades vendidas: {item['quantidade']}")

print(f"\nTempo de resposta: {(fim_tempo - inicio_tempo) * 1000:.2f} ms")

#Consistência Eventual (Eventual Consistency).
#Em arquitetura de software, vivemos de trade-offs (trocas). Nós escolhemos sacrificar a precisão em tempo real (ter dados com até 1 minuto de atraso) para garantir a alta disponibilidade (o sistema não cair sexta-feira à noite). Quando o segundo 61 chegar, o cache expira, o sistema vai ao SQL (Cache Miss), pega as 15 novas vendas, e salva no Redis por mais 60 segundos.