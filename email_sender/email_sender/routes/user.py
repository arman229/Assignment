from email_sender.db_connections import DB_SESSION
from sqlmodel import select
from fastapi import BackgroundTasks, HTTPException, Depends, APIRouter
from pydantic import EmailStr
from itsdangerous import SignatureExpired, BadSignature
from fastapi.security import OAuth2PasswordRequestForm
from email_sender.model.user import *
from email_sender.utils.utils import *
from email_sender.send_mail import *
from datetime import datetime, timedelta


router = APIRouter()


@router.post("/signup")
async def signup(
    user: SignUpForm, background_tasks: BackgroundTasks, session: DB_SESSION
):
    if user:
        exesting_user = session.exec(
            select(UserDB).where(UserDB.email == user.email)
        ).first()
    if exesting_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user = UserDB(
        email=user.email,
        hashed_password=hashed_password,
        is_verified=False,
        username=user.username,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    token = serializer.dumps(user.email, salt="email-confirm")
    background_tasks.add_task(send_verification_email, user.email, token)
    return {
        "message": "Sign-up successful! Please check your email to verify your account."
    }


@router.get("/verify/{token}")
async def verify_email(token: str, session: DB_SESSION):
    try:
        email = serializer.loads(token, salt="email-confirm", max_age=180)
    except SignatureExpired:
        raise HTTPException(
            status_code=400, detail="The confirmation link has expired."
        )
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid confirmation token.")

    user = session.exec(select(UserDB).where(UserDB.email == email)).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    user.is_verified = True
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "Email verified successfully! You can now log in."}


@router.post("/resend_verification")
async def resend_verification(
    session: DB_SESSION, email: EmailStr, background_tasks: BackgroundTasks
):
    user = session.exec(select(UserDB).where(UserDB.email == email)).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")

    if user.is_verified:
        raise HTTPException(status_code=400, detail="Email already verified.")

    token = serializer.dumps(email, salt="email-confirm")

    background_tasks.add_task(send_verification_email, email, token)

    return {"message": "Verification email resent. Please check your inbox."}


@router.post("/signin")
async def signin(
    session: DB_SESSION,
    background_tasks: BackgroundTasks,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    email = form_data.username
    password = form_data.password
    user = session.exec(select(UserDB).where(UserDB.email == email)).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Email is not verified")

    if not pwd_context.verify(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    user.token = access_token
    session.add(user)
    session.commit()
    session.refresh(user)
    login_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    background_tasks.add_task(
        send_login_success_email, user.email, user.username, login_time
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "message": f"Welcome back, {user.username}! A login notification has been sent to your email.",
    }


@router.post("/forgot_password")
async def forgot_password(
    session: DB_SESSION,
    request: PasswordResetRequest,
    background_tasks: BackgroundTasks,
):
    email = request.email
    user = session.exec(select(UserDB).where(UserDB.email == email)).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")

    token = serializer.dumps(email, salt="password-reset")

    background_tasks.add_task(send_password_reset_email, email, token)

    return {"message": "Password reset email sent. Please check your inbox."}


@router.post("/reset_password")
async def reset_password(session: DB_SESSION, data: PasswordResetForm):
    try:
        email = serializer.loads(
            data.token, salt="password-reset", max_age=260
        )  # max_age is in seconds
    except SignatureExpired:
        raise HTTPException(
            status_code=400,
            detail="The reset link has expired. Please request a new one.",
        )
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid reset token.")
    user = session.exec(select(UserDB).where(email == UserDB.email)).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")

    hashed_password = pwd_context.hash(data.password)
    user.hashed_password = hashed_password
    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "message": "Password reset successful. You can now log in with your new password."
    }


@router.put("/user/{user_id}", response_model=UserDB)
async def update_user(
    session: DB_SESSION,
    user_id: int,
    updated_user: SignUpFormUpdate,
    current_user: UserDB = Depends(get_current_user),
):
    user = session.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.role != "admin" and user.email != current_user.email:
        raise HTTPException(
            status_code=403, detail="You do not have permission to update this user"
        )
    if updated_user.username:
        user.username = updated_user.username
    if updated_user.password:
        user.hashed_password = pwd_context.hash(updated_user.password)

    user.updated_at = datetime.utcnow() 
    session.commit()
    session.refresh(user)

    return user


@router.get("/user/me", response_model=UserDB)
async def read_user_me(
    current_user: UserDB = Depends(get_current_user),
):
    return current_user
