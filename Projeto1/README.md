# Web3 

   Projeto 1 - Consulta de saldos na BSC com web3



Pré-requisitos:

-> Acesso à internet (para conectar ao RPC)

-> Python 3.7 >=

-> Python Package Index (pip)

-> setuptolls < 81 

-> Web3.py (biblioteca web3)

-> iphyton para maior interação (opcional)

-> Recomenda-se fortemente, o uso de venv (virtual enviroment)




 Configuração:

 sudo apt install python3 && sudo apt update (instalação e atualização do python3)

 sudo apt install python3-pip (instalação do pip)

 pip install setuptools==80.10.2 (instalar setuptools, necessário ser < 81)

 pip install web3 (instalar biblioteca web3)

 pip install iphyton (instalar iphyton Opcional**)

 python3 -m venv venv && source venv/bin/activate (instalação e ativação do venv)




 Iniciar web3 com "web3.py"

 1. Renomeie  `.env.example` para `.env`

 2. Preencha as variáveis:

   - `RPC_URL`: um dos nós públicos da BSC (ex. binance, defibit, minicoin, publicnode)

   - `WALLET_ADDRESS`: wallet a consultar (ex: Binance Hot Wallet 8, Binace 14, Binance 7, Binance Peg Tokens)

   - `TOKEN_CONTRACT`: contrato do token (ex: USDT, BUSD, CAKE, WBNB )


 Como executar:
 Dentro do command line interface (CLI) digite...


 python3 -m venv venv && source venv/bin/activate        # (inicializa o venv)

 acesse a pasta do projeto (nesse caso:  /web3/Projeto1)

 pip install -r requirement.txt    #(dentro da pasta do projeto para instalar o que é requerido)

 python main.py          #(executa o arquivo main.py)
