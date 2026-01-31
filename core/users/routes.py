from fastapi import APIRouter,Depends,HTTPException,status
from users.schemas import UserRegisterSchema,UserLoginSchema,UserLogoutSchema,UserRefreshTokenSchema
from auth.jwt_cookie_auth import generate_access_token,generate_refresh_token,decode_refresh_token
from sqlalchemy.orm import Session
from core.database import get_db
import secrets
from users.models import UserModel


router = APIRouter(tags=["users"])
async def generate_token(length=32):
    return secrets.token_hex(length)

@router.post("/login")
async def user_login(request: UserLoginSchema, db: Session=Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(
        username=request.username.lower()
        ).first()
    if not user_obj or not user_obj.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_register(request: UserRegisterSchema, db: Session=Depends(get_db)):
    if db.query(UserModel).filter(
        UserModel.username.ilike(request.username)
    ).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= "Username already exist"
        )
    user_obj = UserModel(username=request.username.lower(),first_name=request.first_name,last_name=request.last_name)
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    return {"detail": "User register successfully", "user_id": user_obj.id}

@router.post("/logout")
async def user_logout(request: UserLogoutSchema,db: Session=Depends(get_db)):
    
    return {"detail": "User logged out successfully", "user_id": request.user_id}


@router.post("/refresh-token")
async def refresh_access_token(request: UserRefreshTokenSchema, db: Session=Depends(get_db)):
    try:
        user_id  = decode_refresh_token(request.refresh_token)
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not refresh access token"
        )
    user_obj = db.query(UserModel).filter_by(id=user_id).first()
    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    new_access_token = generate_access_token(user_obj.id)
    return {"access_token": new_access_token, "token_type": "bearer"}