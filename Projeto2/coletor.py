import os
import sys
from web3 import Web3
from datetime import datetime, timezone
from config import RPC_URL, TOKEN_CONTRACT, TOKEN_SYMBOL, WALLETS
from database import SessionLocal, init_db
from models import Balance


TOKEN_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    }
]

def conectar_web3():
    
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        raise ConnectionError(f"Não foi possível conectar ao RPC: {RPC_URL}")
    print(f"Conectado ao RPC: {RPC_URL}")
    return w3

def obter_saldo_token(w3, wallet_address, token_contract, simbolo):
    
    try:
        contract = w3.eth.contract(address=token_contract, abi=TOKEN_ABI)
        decimals = contract.functions.decimals().call()
        saldo_wei = contract.functions.balanceOf(wallet_address).call()
        saldo = saldo_wei / 10**decimals
        print(f"Saldo de {simbolo} para {wallet_address}: {saldo:.6f}")
        return saldo
    except Exception as e:
        print(f"Erro ao obter saldo de {wallet_address}: {e}")
        return None

def coletar_e_salvar():
    """Coleta saldos de todas as wallets e salva no banco."""
    
    init_db()
    db = SessionLocal()
    w3 = conectar_web3()
    
    for wallet in WALLETS:
        saldo = obter_saldo_token(w3, wallet, TOKEN_CONTRACT, TOKEN_SYMBOL)
        if saldo is not None:
            registro = Balance(
                wallet_address=wallet,
                token_symbol=TOKEN_SYMBOL,
                balance=saldo,
                collected_at=datetime.now(timezone.utc)
            )
            db.add(registro)
            print(f"Registro adicionado para {wallet}")
        else:
            print(f"Falha ao obter saldo de {wallet}, não salvo.")
    
    db.commit()
    db.close()
    print("Coleta finalizada. Dados salvos no banco.")

if __name__ == "__main__":
    coletar_e_salvar()
