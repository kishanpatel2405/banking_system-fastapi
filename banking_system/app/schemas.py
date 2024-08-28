from pydantic import BaseModel
from typing import Optional

class AccountBase(BaseModel):
    owner: str
    balance: float
    account_type: str  # or use AccountType if you want to keep it as an enum
    interest_rate: Optional[float] = None

class AccountCreate(AccountBase):
    pass

class UpdateAccount(BaseModel):
    balance: float
    account_type: str  # or use AccountType if you want to keep it as an enum

class AccountResponse(AccountBase):
    id: int
    fee: float

    class Config:
        orm_mode = True

class TransactionResponse(BaseModel):
    id: int
    account_id: int
    amount: float
    timestamp: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    password: str

class UserInDB(BaseModel):
    username: str
    hashed_password: str