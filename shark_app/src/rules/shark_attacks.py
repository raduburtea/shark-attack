from bson import ObjectId
from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError
from src.models.shark_attacks import SharkAttacks, UpdateSharkAttacks


def get_collection_shark_attacks(request: Request):
    return request.app.database["shark_attacks"]


def create_shark_attack(request: Request, shark_attack: SharkAttacks):
    shark_attack = jsonable_encoder(shark_attack)
    new_shark_attack = get_collection_shark_attacks(request).insert_one(shark_attack)
    created_shark_attack = get_collection_shark_attacks(request).find_one(
        {"_id": new_shark_attack.inserted_id}
    )
    return created_shark_attack


def update_shark_attack(request: Request, id: str, shark_attack: UpdateSharkAttacks):
    shark_attack = {k: v for k, v in shark_attack.dict().items() if v is not None}
    if len(shark_attack) >= 1:
        update_result = get_collection_shark_attacks(request).update_one(
            {"id": ObjectId(id)}, {"$set": shark_attack}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Shark attack not found!"
            )

    if (
        existing_shark_attack := get_collection_shark_attacks(request).find_one(
            {"id": ObjectId(id)}
        )
    ) is not None:
        return existing_shark_attack

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Shark attack not found!"
    )


def list_shark_attacks(request: Request, limit=int):
    shark_attacks = list(get_collection_shark_attacks(request).find(limit=limit))
    return shark_attacks


def list_shark_attacks_by_id(request: Request, id: str):
    if shark_attack := get_collection_shark_attacks(request).find_one(
        {"id": ObjectId(id)}
    ):
        return shark_attack
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"shark_attack not found!"
    )


def list_shark_attacks_by_country(request: Request, author: str):
    shark_attacks = list(
        get_collection_shark_attacks(request).aggregate(
            [{"$match": {"country": author}}]
        )
    )
    return shark_attacks


def list_shark_attacks_by_activity(request: Request, author: str):
    shark_attacks = list(
        get_collection_shark_attacks(request).aggregate(
            [{"$match": {"activity": author}}]
        )
    )
    return shark_attacks


def list_shark_attacks_by_type(request: Request, author: str):
    shark_attacks = list(
        get_collection_shark_attacks(request).aggregate([{"$match": {"type": author}}])
    )
    return shark_attacks


def delete_shark_attack(request: Request, id: str):
    deleted_shark_attack = get_collection_shark_attacks(request).delete_one(
        {"id": ObjectId(id)}
    )

    if deleted_shark_attack.deleted_count == 1:
        return f"Shark attack with ID {id} deleted sucessfully!"

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Shark attack not found!"
    )


def delete_invalid_shark_attacks(request: Request, limit=100):
    collection = get_collection_shark_attacks(request).find(limit=limit)
    try:
        invalid_count = 0
        valid_count = 0

        # Get all documents
        all_documents = list(collection)

        for doc in all_documents:
            try:
                # Try to validate document against Pydantic model
                SharkAttacks(**doc)
                valid_count += 1
            except ValidationError:
                # If validation fails, document is invalid
                get_collection_shark_attacks(request).delete_one({"_id": doc["_id"]})
                invalid_count += 1

        return {
            "message": f"Cleanup completed. Removed {invalid_count} invalid documents. {valid_count} valid documents remain."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))