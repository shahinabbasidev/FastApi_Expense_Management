from fastapi import APIRouter,Depends,HTTPException,status,Query
from expenses.schemas import ExpenseResponseSchema
from fastapi.responses import JSONResponse
from users.schemas import UserRegisterSchema
from sqlalchemy.orm import Session,joinedload
from core.database import get_db
from typing import List,Annotated
from expenses.models import ExpenseModel
from users.models import UserModel
from user_expense.schemas import CreateExpenseWithUserSchema


router = APIRouter(tags=["expenses"])


@router.get("/expenses",response_model=List[ExpenseResponseSchema])
async def retrieve_expenses_list(q:Annotated[str | None, Query(max_length=30)] = None,
                                  db:Session=Depends(get_db)
):
    query = (
    db.query(ExpenseModel)
      .options(joinedload(ExpenseModel.users))
)
    if q:
        query = query.filter(ExpenseModel.expense_name.ilike(f"%{q}%"))
    result = query.all()
    return result

@router.get("/expense/{expense_id}",response_model=ExpenseResponseSchema)
async def retrieve_expense_detail(id:int,db:Session=Depends(get_db)):
    expense = db.query(ExpenseModel).filter_by(id=id).one_or_none()
    if expense:
        return expense
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")
    


@router.post("/expenses", response_model=ExpenseResponseSchema)
async def add_expense(
    request: CreateExpenseWithUserSchema,
    db: Session = Depends(get_db)
):
    new_user = UserModel(
        first_name=request.user.first_name,
        last_name=request.user.last_name,
        username=request.user.username,
        password=UserModel.hash_password(request.user.password),
    )
    db.add(new_user)
    db.flush()

    new_expense = ExpenseModel(
        expense_name=request.expense.expense_name,
        mount=request.expense.mount,
    )

    new_expense.users.append(new_user)

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.put("/person-update/{id}",response_model=ExpenseResponseSchema)
async def update_person(id:int,request:CreateExpenseWithUserSchema,db:Session=Depends(get_db)):
    person = db.query(UserModel).filter_by(id=id).one_or_none()
    if person:
        person.first_name = request.user.first_name
        person.last_name = request.user.last_name
        db.commit()
        db.refresh(person)
        return person
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")


@router.delete("/expense/{id}")
async def delete_expense(id:int,db:Session=Depends(get_db)):
    person = db.query(UserModel).filter_by(id=id).one_or_none()
    if person:
        db.delete(person)
        db.commit()
        return JSONResponse(content={"detail":"object remove successfully"},status_code=status.HTTP_200_OK)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="object not found")

