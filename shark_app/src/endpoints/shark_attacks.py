from typing import List

import src.rules.shark_attacks as shark_attacks
from fastapi import APIRouter, Request, status
from src.models.shark_attacks import SharkAttacks, UpdateSharkAttacks

router = APIRouter(
    prefix="/shark_attacks",
    tags=["Shark Attacks"],
)


@router.post(
    "/",
    response_description="Add a shark attack",
    status_code=status.HTTP_201_CREATED,
    response_model=SharkAttacks,
)
def create_shark_attack(request: Request, shark_attack: SharkAttacks):
    return shark_attacks.create_shark_attack(request, shark_attack)


@router.put(
    "/{id}", response_description="Update a shark attack", response_model=SharkAttacks
)
def update_shark_attack(request: Request, id: str, shark_attack: UpdateSharkAttacks):
    return shark_attacks.update_shark_attack(request, id, shark_attack)


@router.get(
    "/",
    response_description="List all shark attacks",
    response_model=List[SharkAttacks],
)
def list_shark_attacks(request: Request):
    return shark_attacks.list_shark_attacks(request, 100)


@router.get(
    "/{id}/",
    response_description="List shark attack by id",
    response_model=SharkAttacks,
)
def list_shark_attacks_by_id(request: Request, id: str):
    return shark_attacks.list_shark_attacks_by_id(request, id)


@router.get(
    "/{id}/{country}/",
    response_description="List shark by country",
    response_model=List[SharkAttacks],
)
def list_shark_attacks_by_country(request: Request, country: str):
    return shark_attacks.list_shark_attacks_by_country(request, country)


@router.get(
    "/{id}/{activity}/",
    response_description="List shark by activity",
    response_model=List[SharkAttacks],
)
def list_shark_attacks_by_activity(request: Request, activity: str):
    return shark_attacks.list_shark_attacks_by_activity(request, activity)


@router.get(
    "/{id}/{type}/",
    response_description="List shark by type",
    response_model=List[SharkAttacks],
)
def list_shark_attacks_by_type(request: Request, type: str):
    return shark_attacks.list_shark_attacks_by_type(request, type)


@router.delete("/{id}", response_description="Delete a shark attack")
def delete_shark_attack(request: Request, id: str):
    return shark_attacks.delete_shark_attack(request, id)


@router.delete("/")
def cleanup_invalid_formats(request: Request):
    return shark_attacks.delete_invalid_shark_attacks(request, 100)
