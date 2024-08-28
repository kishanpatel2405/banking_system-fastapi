from fastapi import FastAPI
from app.routers import accounts_router, transactions_router, transfer_router, balance_router, auth

app = FastAPI()

app.include_router(accounts_router, prefix="/accounts", tags=["accounts"])
app.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
app.include_router(transfer_router, prefix="/transfer", tags=["transfer"])
app.include_router(balance_router, prefix="/balance", tags=["balance"])

app.include_router(auth.router, prefix="/auth", tags=["auth"])