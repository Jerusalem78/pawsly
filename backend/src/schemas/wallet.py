from pydantic import BaseModel, Field, ConfigDict, model_validator
from uuid import UUID
from src.core.enums import TransactionType
from datetime import datetime


class WalletReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    balance: float
    escrow_balance: float

    @model_validator(mode="after")
    def convert_balance(self):
        self.balance = self.balance / 100
        self.escrow_balance = self.escrow_balance / 100
        return self                                         


class DepositRequestSchema(BaseModel):
    amount: int = Field(gt=0)
    @model_validator(mode="after")
    def convert_balance(self):
        self.amount = self.amount * 100
        return self                                         

class TransactionReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    amount: float
    type: TransactionType
    ref_id: UUID | None
    created_at: datetime
    
    @model_validator(mode="after")
    def convert_balance(self):
        self.amount = self.amount / 100
        return self   