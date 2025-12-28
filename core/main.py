from fastapi import FastAPI,HTTPException,status,Depends,Query
from fastapi.responses import JSONResponse
from schemas.user_schema import UserCreateSchema,UserResponseSchema,UserUpdateSchema
from schemas.expense_schema import ExpenseCreateSchema,ExpenseResponseSchema,ExpenseUpdateSchema
from contextlib import asynccontextmanager
from typing import List,Annotated
from database import Base,engine,get_db,User,Expense
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app:FastAPI):
    # Base.metadata.create_all(engine)
    print("Application startup")
    yield
    print("Application shutdown")

app = FastAPI(lifespan = lifespan)



@app.post("/expenses",response_model=(UserResponseSchema,ExpenseCreateSchema))
def create_expense( request:UserCreateSchema,request2:ExpenseCreateSchema,db:Session = Depends(get_db)):
    
    new_person = User(first_name = request.first_name,last_name = request.last_name,age = request.age)
    new_expense = Expense(expense_name = request2.expense_name,mount = request2.mount)
    db.add(new_person)
    db.add(new_expense)
    db.commit()
    
    
    return {
    "first_name": new_person.first_name,
    "last_name": new_person.last_name,
    "age": new_person.age,
    "expense_name": new_expense.expense_name,
    "mount": new_expense.mount
}

@app.get("/expenses",response_model=list[UserResponseSchema])
def get_all_expenses(q:Annotated[str | None, Query(max_length=30)] = None,db:Session = Depends(get_db)):

    query = db.query(User)
    if q:
        query = query.filter_by(first_name = q)
    result = query.all()
    return result


@app.get("/expenses/{id}",response_model=UserResponseSchema)
def get_expense(id:int,db:Session = Depends(get_db)):
    
    person = db.query(User).filter_by(id=id).one_or_none()
    if person:
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")

@app.put("/expenses/{id}",response_model=UserResponseSchema)
def update_list(id:int,request:UserUpdateSchema,db:Session = Depends(get_db)):
    
    person = db.query(User).filter_by(id=id).one_or_none()
    if person:
        person.first_name = request.first_name
        db.commit()
        db.refresh(person)
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")


@app.delete("/expenses/{id}")
def delete_title(id:int,db:Session = Depends(get_db)):
    person = db.query(User).filter_by(id=id).one_or_none()
    if person:
            db.delete(person)
            db.commit()
            return JSONResponse(content={"detail":"object remove successfully"},status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")



