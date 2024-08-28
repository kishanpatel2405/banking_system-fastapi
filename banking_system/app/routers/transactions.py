from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Transaction, User
from datetime import datetime
from app.auth import get_current_user  # Ensure this import is correct

router = APIRouter()

@router.get("/{account_id}")
def get_transaction_history(account_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        transactions = db.query(Transaction).filter(Transaction.account_id == account_id).all()
        if not transactions:
            raise HTTPException(status_code=404, detail="No transactions found for this account.")
        return transactions
    except Exception as e:
        print(f"An error occurred while fetching transactions: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/{account_id}/from/{start_date}/to/{end_date}", response_model=list)
def get_transaction_history_range(account_id: int, start_date: str, end_date: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD HH:MM:SS.")

    try:
        transactions = db.query(Transaction).filter(
            Transaction.account_id == account_id,
            Transaction.timestamp.between(start_date, end_date)
        ).all()

        if not transactions:
            raise HTTPException(status_code=404, detail="No transactions found for this period.")

        return transactions
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        print(f"An unexpected error occurred while fetching transactions for range: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
