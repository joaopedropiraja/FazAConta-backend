from enum import Enum


class TransactionType(str, Enum):
    SEND = "send"
    EXPENSE = "expense"
    REIMBURSEMENT = "reimbursement"
