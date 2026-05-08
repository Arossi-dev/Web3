import os
from dotenv import load_dotenv
from web3 import Web3


# Carrega variáveis do .env
load_dotenv()

WALLET_ADDRESS = os.getenv("WALLET_ADDRESS")
TOKEN_CONTRACT = os.getenv("TOKEN_CONTRACT")

if not WALLET_ADDRESS or not TOKEN_CONTRACT:
    raise ValueError("Variáveis WALLET_ADDRESS e TOKEN_CONTRACT devem estar no .env")

# Lista de RPCs públicos da BSC (com timeout)
RPC_URLS = [
    "https://bsc-dataseed.binance.org/",
    "https://bsc-dataseed1.defibit.io/",
    "https://bsc-dataseed1.ninicoin.io/",
    "https://bsc.publicnode.com/"
]

def conectar_bsc():
    """Tenta conectar aos RPCs em sequência. Retorna Web3 conectado."""
    for rpc in RPC_URLS:
        try:
            w3 = Web3(Web3.HTTPProvider(rpc, request_kwargs={'timeout': 5}))
            if w3.is_connected():
                print(f"Conectado ao RPC: {rpc}")
                return w3
        except Exception as e:
            print(f"Falha ao conectar a {rpc}: {e}")
    raise ConnectionError("Não foi possível conectar a nenhum RPC da BSC.")

def obter_saldo_token(w3, endereco_wallet, contrato_token):
    """Retorna saldo do token (float) e símbolo (string)."""
    # ABI mínima para balanceOf e decimals
    abi = [
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
        },
        {
            "constant": True,
            "inputs": [],
            "name": "symbol",
            "outputs": [{"name": "", "type": "string"}],
            "type": "function"
        }
    ]
    contrato = w3.eth.contract(address=contrato_token, abi=abi)
    saldo_wei = contrato.functions.balanceOf(endereco_wallet).call()
    decimais = contrato.functions.decimals().call()
    simbolo = contrato.functions.symbol().call()
    return saldo_wei / 10**decimais, simbolo

def main():
    # Conecta
    w3 = conectar_bsc()
    
    # 1. Bloco atual
    bloco = w3.eth.block_number
    print(f"Bloco atual da BSC: {bloco}")
    
    # 2. Saldo BNB nativo
    saldo_bnb_wei = w3.eth.get_balance(WALLET_ADDRESS)
    saldo_bnb = saldo_bnb_wei / 10**18
    print(f"Saldo de BNB da wallet {WALLET_ADDRESS}: {saldo_bnb:.6f} BNB")
    
    # 3. Saldo do token
    try:
        saldo_token, simbolo = obter_saldo_token(w3, WALLET_ADDRESS, TOKEN_CONTRACT)
        print(f"Saldo do token {simbolo} na mesma wallet: {saldo_token:.6f} {simbolo}")
    except Exception as e:
        print(f"Erro ao obter saldo do token: {e}")
        print("Verifique o endereço do contrato e se a wallet possui esse token.")

if __name__ == "__main__":
    main()
