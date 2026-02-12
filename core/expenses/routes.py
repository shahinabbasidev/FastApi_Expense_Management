from fastapi import APIRouter, Depends, HTTPException, status, Query
from expenses.schemas import ExpenseResponseSchema, BaseExpenseSchema
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.database import get_db
from typing import List
from expenses.models import ExpenseModel
from users.models import UserModel
from auth.jwt_cookie_auth import get_authenticated_user
from messages.auth import Messages

router = APIRouter(tags=["expenses"])


@router.get("/expenses", response_model=List[ExpenseResponseSchema])
async def retrieve_expenses_list(
    completed: bool = Query(
        None, description="Filter expenses based on being completed or no"
    ),
    limit: int = Query(
        10, gt=0, le=50, description="Limiting the number of items to retrieve"
    ),
    offset: int = Query(
        0, gt=-1, description="Use for paginating based on passed items"
    ),
    user: UserModel = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    query = db.query(ExpenseModel).filter_by(user_id=user.id)
    if completed is not None:
        query = query.filter_by(is_complete=completed)

    return query.limit(limit).offset(offset).all()


@router.get("/expense/{expense_id}", response_model=ExpenseResponseSchema)
async def retrieve_expense_detail(
    id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    expense = (
        db.query(ExpenseModel).filter_by(user_id=user.id, id=id).one_or_none()
    )
    if expense:
        return expense
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Messages.expense_not_found(),
        )


@router.post("/expenses", response_model=ExpenseResponseSchema)
async def add_expense(
    request: BaseExpenseSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):

    data = request.model_dump()
    data.update({"user_id": user.id})
    expense_obj = ExpenseModel(**data)
    db.add(expense_obj)
    db.commit()
    db.refresh(expense_obj)
    return expense_obj


@router.put("/expense_update/{id}", response_model=ExpenseResponseSchema)
async def update_expense(
    id: int,
    request: BaseExpenseSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    expense = (
        db.query(ExpenseModel).filter_by(user_id=user.id, id=id).one_or_none()
    )
    if expense:
        expense.expense_name = request.expense_name
        expense.mount = request.mount
        db.commit()
        db.refresh(expense)
        return expense
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=Messages.expense_not_found(),
        )


@router.delete("/expense/{id}")
async def delete_expense(
    id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):

    expense = (
        db.query(ExpenseModel).filter_by(user_id=user.id, id=id).one_or_none()
    )
    if expense:
        db.delete(expense)
        db.commit()
        return JSONResponse(
            content={"detail": Messages.expense_removed_successfully()},
            status_code=status.HTTP_200_OK,
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=Messages.expense_not_found(),
    )
