# Dashboard Restaurante 🍽️

Um projeto de dashboard fullstack simples e eficiente para visualizar dados e estatísticas de vendas de um restaurante. O projeto é composto por uma API construída em Python (FastAPI) e um Frontend rápido e moderno feito com TypeScript, Vite e Chart.js.

## Tecnologias Utilizadas

- **Backend:** Python, FastAPI, Uvicorn
- **Banco de Dados:** SQLite
- **Cache (Opcional):** Redis (para otimização de consultas)
- **Frontend:** TypeScript, Vite, Chart.js

## Estrutura do Projeto

O repositório é dividido nas seguintes partes principais:

- `/api`: Contém o servidor backend (`server.py`) responsável por fornecer os endpoints de dados e servir a aplicação web.
- `/frontend`: Aplicação web que exibe os gráficos de vendas e consome a API.
- `gerador_dados.py` & `banco_sql.py`: Scripts utilitários para gerar dados fictícios de vendas e popular o banco de dados local.
- `restaurante.db`: Banco de dados SQLite pré-populado.
- `cache_redis.py`: Exemplo isolado de como o cache do Redis é implementado.

## Como Executar o Projeto

Siga as etapas abaixo para rodar o projeto localmente:

### 1. Pré-requisitos

- [Python 3.x](https://www.python.org/downloads/) instalado.
- [Node.js e npm](https://nodejs.org/) instalados.
- (Opcional) Instância do [Redis](https://redis.io/) rodando na porta 6379 local para testar a funcionalidade de cache.

### 2. Configurando o Backend (API)

No diretório raiz do projeto, instale as dependências do Python:

```bash
pip install -r api/requirements.txt
```

### 3. Configurando o Frontend

Entre na pasta do frontend, instale as dependências e faça o build da aplicação:

```bash
cd frontend
npm install
npm run build
cd ..
```

_(O `build` gera a pasta `dist`, que o servidor FastAPI lê e hospeda automaticamente)._

### 4. Iniciando o Servidor

Volte para a pasta raiz (se necessário) e inicie o servidor Python:

```bash
cd api
python server.py
```

O servidor iniciará e o dashboard estará acessível no seu navegador através do endereço:  
**[http://localhost:3001](http://localhost:3001)**

---

## Geração de Dados

O projeto já acompanha um arquivo `restaurante.db` populado. Caso você queira zerar o banco ou gerar novas vendas aleatórias no futuro (simulando os últimos 90 dias), basta rodar:

```bash
python gerador_dados.py
python banco_sql.py
```

Isso criará um novo arquivo `vendas_restaurante.csv` e em seguida atualizará o banco de dados.
