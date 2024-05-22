"""Coworking Client Reservation API

This API is used to make and manage reservations."""

from fastapi import APIRouter, Depends, HTTPException
from ..authentication import registered_user
from ...services.coworking.reservation import ReservationService
from ...models import User
from ...models.coworking import (
    Reservation,
    ReservationRequest,
    ReservationPartial,
    ReservationState,
    CheckReservationsRequest,
)

__authors__ = ["Kris Jordan"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


api = APIRouter(prefix="/api/coworking")
openapi_tags = {
    "name": "Coworking",
    "description": "Coworking reservations, status, and XL Ambassador functionality.",
}


@api.post("/reservation", tags=["Coworking"])
def draft_reservation(
    reservation_request: ReservationRequest,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    """Draft a reservation request."""
    return reservation_svc.draft_reservation(subject, reservation_request)


@api.get("/reservation/{id}", tags=["Coworking"])
def get_reservation(
    id: int,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    return reservation_svc.get_reservation(subject, id)


@api.put("/reservation/{id}", tags=["Coworking"])
def update_reservation(
    reservation: ReservationPartial,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    """Modify a reservation."""
    return reservation_svc.change_reservation(subject, reservation)


@api.delete("/reservation/{id}", tags=["Coworking"])
def cancel_reservation(
    id: int,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> Reservation:
    """Cancel a reservation."""
    return reservation_svc.change_reservation(
        subject, ReservationPartial(id=id, state=ReservationState.CANCELLED)
    )


@api.post("/reservation/check", tags=["Coworking"])
def check_users_in_reservations(
    request: CheckReservationsRequest,
    subject: User = Depends(registered_user),
    reservation_svc: ReservationService = Depends(),
) -> str:
    """Check if any user in the provided list of pids is in any reservations."""
    return reservation_svc.check_users_in_reservations(subject, request.pids)