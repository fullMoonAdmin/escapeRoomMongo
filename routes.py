from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import GameRecord, GameRecordUpdate

router = APIRouter()

@router.post("/", response_description="Create a new record", status_code=status.HTTP_201_CREATED, response_model=GameRecord)
def create_records(request: Request, record: GameRecord = Body(...)):
    record = jsonable_encoder(record)
    new_record = request.app.database["bankJobData"].insert_one(record)
    created_record = request.app.database["bankJobData"].find_one(
        {"_id": new_record.inserted_id}
    )

    return created_record

@router.get("/", response_description="List all records", response_model=List[GameRecord])
def list_records(request: Request):
    records = list(request.app.database["bankJobData"].find(limit=100))
    return records

@router.get("/{id}", response_description="Get a single record by id", response_model=GameRecord)
def find_record(id: str, request: Request):
    if (record := request.app.database["bankJobData"].find_one({"_id": id})) is not None:
        return record
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record with ID {id} not found")

@router.put("/{id}", response_description="Update a record", response_model=GameRecord)
def update_record(id: str, request: Request, record: GameRecordUpdate = Body(...)):
    record = {k: v for k, v in record.dict().items() if v is not None}
    if len(record) >= 1:
        update_result = request.app.database["bankJobData"].update_one(
            {"_id": id}, {"$set": record}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record with ID {id} not found")

    if (
        existing_record := request.app.database["bankJobData"].find_one({"_id": id})
    ) is not None:
        return existing_record

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record with ID {id} not found")

@router.delete("/{id}", response_description="Delete a record")
def delete_record(id: str, request: Request, response: Response):
    delete_result = request.app.database["bankJobData"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Record with ID {id} not found")