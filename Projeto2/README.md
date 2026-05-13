Projeto 2 - Coletor de saldos BSC + PostgreSQL + API FastAPI

Esse projeto coleta saldos de tokens BEP-20 de carteiras públicas, armazena os dados em PostgreSQL e oferece uma API REST para consulta.

 Funcionalidades:

-> Coleta manual (ou agendavel) dos saldos de pelo menos 3 wallets para um token BEP-20 (ex: USDT)
-> Armazenamento em PostgreSQL com modelo de serie temporal (historico)
-> API FastAPI com três endpoints obrigatorios:

  - GET /balances/latest - ultimos saldos de todas as wallets
  - GET /balances/{wallet}/history - historico de uma wallet especifica
  - GET /stats - estatisticas: wallet com maior saldo e variacao percentual nas ultimas 24h
  
-> Documentacao interativa via Swagger em /docs
-> Tolerancia a falhas: fallback entre multiplos RPCs da BSC

 Tecnologias utilizadas:

-> Python 3.12 (recomendado)
-> Web3.py - interacao com a blockchain BSC
-> PostgreSQL - banco de dados relacional
-> SQLAlchemy - ORM e gerenciamento de schema
-> FastAPI - framework para a API
-> Uvicorn - servidor ASGI
-> python-dotenv - gerenciamento de variaveis de ambiente


 Arquitetura do sistema:

Coletor -> RPC BSC -> PostgreSQL <- API FastAPI <- Cliente/Swagger

-> O coletor é um script Python que consulta a blockchain via web3.py e insere os saldos no banco de dados

-> O banco guarda todas as coletas com timestamp, permitindo consultas históricas

-> A API expõe esses dados atraves de endpoints REST, lendo diretamente do banco


 Pre-requisitos:

-> Python 3.12 ou superior
-> PostgreSQL instalado e rodando (localmente ou via Docker)
-> Acesso a internet (para os RPCs da BSC)
-> pip e venv disponiveis


 Configuração:

1. Clone o repositorio e entre na pasta do projeto

cd web3/projeto2


2. Crie e ative um ambiente virtual

python -m venv venv && source venv/bin/activate  

    
3. Instale as dependencias

pip install -r requirements.txt


4. Configure o banco de dados PostgreSQL

4.1. Inicie o PostgreSQL

sudo systemctl start postgresql


4.2. Crie um banco de dados e um usuário

Acesse o terminal do PostgreSQL

sudo -u postgres psql -p 5433


Dentro do psql, execute:

CREATE USER meuuser WITH PASSWORD 'minhasenha';
CREATE DATABASE monitor OWNER meuuser;
GRANT ALL PRIVILEGES ON DATABASE monitor TO meuuser;


(Nota: A porta padrão do PostgreSQL e 5432, mas o seu cluster ativo pode estar em 5433. Ajuste conforme sua instalacao.)



5. Configure as variaveis de ambiente:

Renomeie o arquivo de exemplo.

.env.example para .env

Edite o .env com seus dados reais:

RPC_URL=https://bsc-dataseed.binance.org/
TOKEN_CONTRACT=0x55d398326f99059fF775485246999027B3197955
TOKEN_SYMBOL=USDT
WALLETS=0xF977814e90dA44bFA03b6295A0616a897441aceC,0x28C6c06298d514Db089934071355E5743bf21d60,0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE
DB_HOST=localhost
DB_PORT=5433
DB_NAME=monitor
DB_USER=meuuser
DB_PASSWORD=minhasenha


Como executar:

1. Executar o coletor (pela primeira vez)

O coletor criará automaticamente a tabela balances e inserira os saldos atuais.

python coletor.py


Saida esperada:

Conectado ao RPC: https://bsc-dataseed.binance.org/
Saldo de USDT para 0xF977814e...: 1.316166
Registro adicionado para 0xF977814e...
Coleta finalizada. Dados salvos no banco.

Dica: Para gerar dados históricos, execute o coletor varias vezes em momentos diferentes.



2. Verificar os dados no banco (opcional):

psql -h localhost -p 5433 -U meuuser -d monitor -c "SELECT * FROM balances;"



3. Iniciar a API FastAPI:

python main.py

O servidor sera iniciado em http://0.0.0.0:8000



4. Acessar a documentação interativa (Swagger):

Abra o navegador e digite: http://localhost:8000/docs

Você verá os três endpoints documentados e poderá testa-los diretamente.



5. Testar os endpoints com curl (opcional):

Últimos saldos:
curl http://localhost:8000/balances/latest

Histórico de uma wallet:
curl http://localhost:8000/balances/0xF977814e90dA44bFA03b6295A0616a897441aceC/history

Estatisticas:
curl http://localhost:8000/stats



Estrutura dos arquivos:

-> config.py - Carrega variaveis do .env e exporta configuracoes
-> models.py - Define a tabela balances usando SQLAlchemy
-> database.py - Cria a engine, sessões e função init_db()
-> coletor.py - Conecta a BSC, consulta saldos e insere no banco
-> api.py - Contem os endpoints FastAPI e a logica de consulta
-> main.py - Ponto de entrada para rodar a API com Uvicorn
-> .env - Configuracoes especificas (não commitado)
-> .env.example - Exemplo das variaveis necessarias
-> requirements.txt - Lista de dependencias
