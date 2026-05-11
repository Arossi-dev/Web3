from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db, init_db
from models import Balance
from config import WALLETS, TOKEN_SYMBOL

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    init_db()
    print("✅ Tabelas verificadas/criadas. API pronta!")
    yield
    
    print("🛑 Encerrando a aplicação...")

app = FastAPI(
    title="Monitor de Wallets BSC",
    description="API para consultar saldos históricos de tokens BEP-20",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/balances/latest")
def get_latest(db: Session = Depends(get_db)):
    """
    Retorna os saldos mais recentes de todas as wallets monitoradas.
    """
    
    subq = db.query(
        Balance.wallet_address,
        func.max(Balance.collected_at).label("latest_time")
    ).group_by(Balance.wallet_address).subquery()
    
    results = db.query(Balance).join(
        subq,
        (Balance.wallet_address == subq.c.wallet_address) &
        (Balance.collected_at == subq.c.latest_time)
    ).all()
    
    return results

@app.get("/balances/{wallet}/history")
def get_history(wallet: str, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retorna o histórico de uma wallet específica (últimos 'limit' registros).
    """
    history = db.query(Balance).filter(Balance.wallet_address == wallet).order_by(Balance.collected_at.desc()).limit(limit).all()
    if not history:
        raise HTTPException(status_code=404, detail="Wallet não encontrada")
    return history

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """
    Estatísticas: wallet com maior saldo atual e variação percentual das últimas 24h.
    """
   
    subq = db.query(
        Balance.wallet_address,
        func.max(Balance.collected_at).label("latest_time")
    ).group_by(Balance.wallet_address).subquery()
    
    latest_balances = db.query(Balance).join(
        subq,
        (Balance.wallet_address == subq.c.wallet_address) &
        (Balance.collected_at == subq.c.latest_time)
    ).all()
    
    if not latest_balances:
        return {"error": "Sem dados no banco"}
    
    maior = max(latest_balances, key=lambda x: x.balance)
    
   
    agora = datetime.utcnow()
    dia_atras = agora - timedelta(hours=24)
    detalhes = []
    
    for wallet in WALLETS:
        ultimo = db.query(Balance).filter(Balance.wallet_address == wallet).order_by(Balance.collected_at.desc()).first()
        antigo = db.query(Balance).filter(
            Balance.wallet_address == wallet,
            Balance.collected_at <= dia_atras
        ).order_by(Balance.collected_at.desc()).first()
        
        variacao = None
        if ultimo and antigo and antigo.balance != 0:
            variacao = ((ultimo.balance - antigo.balance) / antigo.balance) * 100
        
        detalhes.append({
            "wallet": wallet,
            "ultimo_saldo": float(ultimo.balance) if ultimo else None,
            "variacao_24h_percent": round(variacao, 2) if variacao is not None else None
        })
    
    return {
        "wallet_com_maior_saldo": maior.wallet_address,
        "detalhes_variacao": detalhes
    }
