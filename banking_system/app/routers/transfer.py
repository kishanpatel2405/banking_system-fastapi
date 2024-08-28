from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Account

router = APIRouter()

@router.post("/transfer")
def transfer(from_account_id: int, to_account_id: int, amount: float, db: Session = Depends(get_db)):
    from_account = db.query(Account).filter(Account.id == from_account_id).first()
    to_account = db.query(Account).filter(Account.id == to_account_id).first()

    if not from_account or not to_account:
        raise HTTPException(status_code=404, detail="Account not found")

    if from_account.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    from_account.balance -= amount
    to_account.balance += amount

    db.commit()

    return {"message": "Transfer successful", "from_balance": from_account.balance, "to_balance": to_account.balance}
