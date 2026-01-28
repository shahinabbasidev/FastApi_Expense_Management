from fastapi import APIRouter,Depends,HTTPException,status
from users.schemas import UserRegisterSchema,UserLoginSchema,UserLogoutSchema
from sqlalchemy.orm import Session
from core.database import get_db
import secrets
from users.models import UserModel


router = APIRouter()
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
    

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def user_register(request: UserRegisterSchema, db: Session=Depends(get_db)):
    if db.query(UserModel).filter(
        UserModel.username.ilike(request.username)
    ).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail= "Username already exist"
        )
    user_obj = UserModel(username=request.username.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    return {"detail": "User register successfully", "user_id": user_obj.id}

@router.post("/logout")
async def user_logout(request: UserLogoutSchema,db: Session=Depends(get_db)):
    
    return{}