import os
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
TOKEN_CONTRACT = os.getenv("TOKEN_CONTRACT")
TOKEN_SYMBOL = os.getenv("TOKEN_SYMBOL")

# Lê as wallets separadas por vírgula
WALLETS = [w.strip() for w in os.getenv("WALLETS", "").split(",") if w.strip()]

# Banco de dados
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
