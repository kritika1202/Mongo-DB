import os
from contextlib import asynccontextmanager
from datetime import date, datetime, time
from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import FastAPI, HTTPException, Request, Response, status
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field
from pymongo.errors import DuplicateKeyError


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
    try:
        app.state.employees = client.employee_db.employees
        app.state.employee_records = client.employee_db.employee
        await app.state.employees.create_index("email", unique=True)
        yield
    finally:
        client.close()


app = FastAPI(title="Employee Management API", lifespan=lifespan)


class EmployeeInput(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    department: str = Field(..., min_length=1)
    position: str = Field(..., min_length=1)
    salary: float = Field(..., ge=0, allow_inf_nan=False)
    date_joined: date | None = None


class EmployeeOutput(EmployeeInput):
    id: str


class EmployeeRecord(BaseModel):
    id: int
    name: str
    age: int
    salary: float
    desig: str


def parse_id(employee_id: str) -> ObjectId:
    try:
        return ObjectId(employee_id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Invalid employee ID")


def document_for(employee: EmployeeInput) -> dict[str, Any]:
    document = employee.model_dump()
    if document["date_joined"] is not None:
        document["date_joined"] = datetime.combine(document["date_joined"], time.min)
    return document


def employee_for_response(document: dict[str, Any]) -> dict[str, Any]:
    document = dict(document)
    document["id"] = str(document.pop("_id"))
    if isinstance(document.get("date_joined"), datetime):
        document["date_joined"] = document["date_joined"].date()
    return document


@app.post("/add", status_code=201)
async def add_employee_record(employee: EmployeeRecord, request: Request):
    await request.app.state.employee_records.insert_one(employee.model_dump())
    return {"message": "Employee added successfully"}


@app.get("/getAll", response_model=list[EmployeeRecord])
async def get_all_employee_records(request: Request):
    return [
        document
        async for document in request.app.state.employee_records.find(
            {}, {"_id": 0}
        )
    ]


@app.post("/employees", response_model=EmployeeOutput, status_code=201)
async def create_employee(employee: EmployeeInput, request: Request):
    document = document_for(employee)
    try:
        result = await request.app.state.employees.insert_one(document)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Employee email already exists")
    document["_id"] = result.inserted_id
    return employee_for_response(document)


@app.get("/employees", response_model=list[EmployeeOutput])
async def list_employees(request: Request):
    return [
        employee_for_response(document)
        async for document in request.app.state.employees.find()
    ]


@app.get("/employees/{employee_id}", response_model=EmployeeOutput)
async def get_employee(employee_id: str, request: Request):
    document = await request.app.state.employees.find_one(
        {"_id": parse_id(employee_id)}
    )
    if document is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_for_response(document)


@app.put("/employees/{employee_id}", response_model=EmployeeOutput)
async def update_employee(
    employee_id: str, employee: EmployeeInput, request: Request
):
    object_id = parse_id(employee_id)
    document = document_for(employee)
    try:
        result = await request.app.state.employees.replace_one(
            {"_id": object_id}, document
        )
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Employee email already exists")
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    document["_id"] = object_id
    return employee_for_response(document)


@app.delete("/employees/{employee_id}", status_code=204)
async def delete_employee(employee_id: str, request: Request):
    result = await request.app.state.employees.delete_one(
        {"_id": parse_id(employee_id)}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
