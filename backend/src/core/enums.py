from enum import Enum

class Role(Enum):
    OWNER = "owner"
    SITTER = "sitter"
    ADMIN = "admin"

class ListingStatus(Enum):
    OPEN = "open"
    MATCHED = "matched"
    CLOSED = "closed"

class ApplicationStatus(Enum): 
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class BookingStatus(Enum):
    PENDING_PAYMENT = "pending_payment"
    ESCROWED = "escrowed"
    SITTER_DONE = "sitter_done"
    COMPLETED = "completed"
    DISPUTED = "disputed"
    RESOLVED_OWNER = "resolved_owner"
    RESOLVED_SITTER = "resolved_sitter"
    RESOLVED_SPLIT = "resolved_split"
    CANCELLED = "cancelled"

class TransactionType(Enum):
    DEPOSIT = "deposit"
    ESCROW_HOLD = "escrow_hold"
    ESCROW_RELEASE = "escroed_release"
    PAYOUT = "payout"
    REFUND = "refund"
    SPLIT_PAYOUT = "split_payout"
    SPLIT_REFUND = "split_refund"

class DisputeStatus(Enum):
    OPEN = "open"
    RESOLVED_OWNER = "resolved_owner"
    RESOLVED_SITTER = "resolved_sitter"
    RESOLVED_SPLIT = "resolved_split"

class Spicies(Enum):
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    RODENT = "rodent"
    REPTILE = "reptile"
    OTHER = "other"