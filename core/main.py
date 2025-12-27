from fastapi import FastAPI,HTTPException,status,Depends,Query
from fastapi.responses import JSONResponse
import random
from schemas import PersonCreateSchema,PersonResponseSchema,PersonUpdateSchema
from contextlib import asynccontextmanager
from typing import List,Annotated
from database import Base,engine,get_db,User,Expense
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")

app = FastAPI(lifespan = lifespan)

expenses_list = []


@app.post("/expenses",response_model=PersonResponseSchema)
def create_expense( person:PersonCreateSchema,db:Session = Depends(get_db)):
    # expense_obj = {"id":random.randint(1,1000),"title":person.title,"mount": person.mount}
    # expenses_list.append(expense_obj)
    new_person = User(first_name = person.title,mount=person.mount)
    db.add(new_person)
    db.close()
    db.refresh()
    return JSONResponse(content=new_person,status_code=status.HTTP_201_CREATED)

@app.get("/expenses",response_model=list[PersonResponseSchema])
def get_all_expenses(q:Annotated[str | None, Query(max_length=30)] = None,db:Session = Depends(get_db)):

    query = db.query(User)
    if q:
        query = query.filter_by(User.first_name)
    result = query.all()
    return JSONResponse(content=result,status_code=status.HTTP_200_OK)


@app.get("/expenses/{id}",response_model=PersonResponseSchema)
def get_expense(id:int):
    for item in expenses_list:
        if item["id"] == id:
            return JSONResponse(content=item,status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")

@app.put("/expenses/{id}",response_model=PersonResponseSchema)
def update_list(id:int,person:PersonUpdateSchema):
    for item in expenses_list:
        if item["id"] == id:
            item["title"] = person.title
            return JSONResponse(content={"detail":"object update successfully"},status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")


@app.delete("/expenses/{id}")
def delete_title(id:int):
    for item in expenses_list:
        if item["id"] == id:
            expenses_list.remove(item)
            return JSONResponse(content={"detail":"object remove successfully"},status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")



