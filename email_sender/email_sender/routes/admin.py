from fastapi import APIRouter
from email_sender.model.user import *
from email_sender.utils.utils import *
from email_sender.db_connections import *

adminrouter = APIRouter()


# @adminrouter.get("/admin")
# async def read_admin_data(current_admin_user: User = Depends(get_current_admin_user)):
#     return {"message": "Welcome Admin! This is your exclusive data."}

@adminrouter.get("/admin/all_users")
async def list_of_users( session:DB_SESSION,current_admin_user: UserDB = Depends(get_current_admin_user)):
    users = session.exec(select(UserDB)).all()
    return users

@adminrouter.delete("/admin/users/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    session: DB_SESSION,
    current_admin_user: UserDB = Depends(get_current_admin_user)
):
    user = session.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit() 
    return {"message": f"User with ID {user_id} has been deleted."}


@adminrouter.post("/admin/user/create", response_model=UserDB)
async def create_user(
    user: SignUpForm, 
    session: DB_SESSION,
    current_admin_user: UserDB = Depends(get_current_admin_user)
):
     
    if user:
        exesting_user = session.exec(select(UserDB).where(UserDB.email==user.email)).first()
    if exesting_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user = UserDB(email=user.email, hashed_password=hashed_password,is_verified=True,username=user.username)
    session.add(new_user)
    session.commit()
    session.refresh(new_user) 
    return new_user
 