from src.core.enums import BookingStatus, ListingStatus, ApplicationStatus
from src.core.exceptions import BadRequestException


BOOKING_TRANSITIONS = {
    BookingStatus.PENDING_PAYMENT: [BookingStatus.ESCROWED, BookingStatus.CANCELLED],
    BookingStatus.ESCROWED: [BookingStatus.SITTER_DONE, BookingStatus.CANCELLED],
    BookingStatus.SITTER_DONE: [BookingStatus.COMPLETED, BookingStatus.DISPUTED],
    BookingStatus.DISPUTED: [BookingStatus.RESOLVED_OWNER, BookingStatus.RESOLVED_SITTER, BookingStatus.RESOLVED_SPLIT],
}

LISTING_TRANSITION = {
    ListingStatus.OPEN : [ListingStatus.MATCHED, ListingStatus.CLOSED],
    ListingStatus.MATCHED : [ListingStatus.CLOSED]
}

APPLICATION_TRANSITION = {
    ApplicationStatus.PENDING : [ApplicationStatus.ACCEPTED, ApplicationStatus.REJECTED],
}


def validate_transition(transition : dict, current, new) -> None:
    allowed = transition.get(current, [])
    if new not in allowed:
        raise BadRequestException(f"Переход из {current} в {new} недопустим")



