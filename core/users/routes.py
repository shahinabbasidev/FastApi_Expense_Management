from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from users.schemas import UserRegisterSchema, UserLoginSchema
from auth.jwt_cookie_auth import generate_access_token, generate_refresh_token, decode_refresh_token
from users.schemas import UserRegisterSchema, UserResponseSchema, UserUpdateResponseSchema
from sqlalchemy.orm import Session
from core.database import get_db
import secrets
from users.models import UserModel
from auth.jwt_cookie_auth import get_authenticated_user
from messages.auth import Messages
from i18n.translator import _

router = APIRouter(tags=["users"])


def generate_token(length=32):
    return secrets.token_hex(length)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter(
        UserModel.username.ilike(request.username)
    ).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=Messages.user_already_exists()
        )

    if not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=Messages.password_missing()
        )

    user_obj = UserModel(username=request.username.lower(
    ), first_name=request.first_name, last_name=request.last_name)
    user_obj.set_password(request.password)

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    return {"detail": Messages.registered_successfully(), "user_id": user_obj.id}


@router.post("/login")
async def user_login(
    request: UserLoginSchema,
    response: Response,
    db: Session = Depends(get_db)
):
    user_obj = db.query(UserModel).filter_by(
        username=request.username.lower()
    ).first()
    if not user_obj:
        raise HTTPException(status_code=404, detail=Messages.user_not_found())

    if not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=401, detail=Messages.invalid_credentials())

    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=60*5
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=3600*24
    )

    return {"detail": Messages.logged_in_successfully()}


@router.post("/refresh-token")
async def refresh_access_token(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No refresh token")

    user_id = decode_refresh_token(refresh_token)

    user_obj = db.query(UserModel).filter_by(id=user_id).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=Messages.user_not_found())

    new_access_token = generate_access_token(user_obj.id)

    response.set_cookie(
        key="access_token",
        value=new_access_token,
        httponly=True,
        max_age=60*5,
        samesite="Lax",
        path="/"
    )

    return {"detail": Messages.token_refreshed_successfully()}


@router.post("/logout")
async def user_logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"detail": Messages.logged_out_successfully()}


@router.put("/user-update", response_model=UserUpdateResponseSchema)
async def update_user(
    request: UserRegisterSchema,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user)
):
    db_user = db.query(UserModel).filter(UserModel.id == user.id).one_or_none()

    if not db_user:
        raise HTTPException(status_code=404, detail=Messages.user_not_found())

    db_user.first_name = request.first_name
    db_user.last_name = request.last_name

    db.commit()
    db.refresh(db_user)

    return {"detail": Messages.updated_successfully(), "user": db_user}
