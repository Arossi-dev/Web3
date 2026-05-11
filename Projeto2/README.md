Projeto 2 – Coletor de saldos BSC + API

Este projeto coleta saldos de tokens BEP‑20 de carteiras públicas, armazena os dados em PostgreSQL e oferece uma API REST para consulta.

# Pré‑requisitos

-> Python 3.12 >=
-> PostgreSQL em execução (local ou Docker)
-> Acesso à internet

# Estrutura dos serviços

| Serviço          | Arquivo a executar               | O que faz                                 |
|------------------|----------------------------------|-------------------------------------------|
| Coletor de dados |  python coletor.py               | Consulta saldos na BSC e salva no banco.  | 
| API REST         |  python main.py ou uvicorn       | Disponibiliza endpoints para consulta.    |

-> Nota: Os dois serviços são independentes. O coletor pode rodar várias vezes (manual ou agendado). A API fica em execução contínua.

# Passo a passo para ativar os serviços

# 1 Configurar o ambiente


# Clone o repositório e entre na pasta do projeto

Crie e ative o ambiente virtual:

python -m venv venv && source venv/bin/activate      
       

Instale as dependências:

pip install -r requirements.txt
