from fastapi import FastAPI,HTTPException,status,Depends,Query
from fastapi.responses import JSONResponse
from user_schema import UserCreateSchema,UserResponseSchema,UserUpdateSchema
from expense_schema import ExpenseCreateSchema,ExpenseResponseSchema,ExpenseUpdateSchema
from contextlib import asynccontextmanager
from typing import List,Annotated
from database import Base,engine,get_db,User,Expense
from sqlalchemy.orm import Session
from user_expense_schema import CreateExpenseWithUserSchema






@asynccontextmanager
async def lifespan(app:FastAPI):
    # Base.metadata.create_all(engine)
    print("Application startup")
    yield
    print("Application shutdown")

app = FastAPI(lifespan = lifespan)



@app.post("/expenses",response_model=CreateExpenseWithUserSchema)
def create_expense( request:CreateExpenseWithUserSchema,db:Session = Depends(get_db)):
    
    new_person = User(first_name = request.user.first_name,last_name = request.user.last_name,age = request.user.age)
    db.add(new_person)
    db.commit()
    new_expense = Expense(expense_name = request.expense.expense_name,mount = request.expense.mount)
    db.add(new_expense)
    db.commit()
    return {
    "user": new_person,
    "expense": new_expense
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



