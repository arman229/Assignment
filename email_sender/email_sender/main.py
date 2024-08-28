from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_sender.settings import EMAIL_PASSWORD,SENDER_EMAIL,SECRET_KEY
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI() 

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
 
serializer = URLSafeTimedSerializer(SECRET_KEY)
 
fake_db = {}
 
class User(BaseModel):
    email: EmailStr
    password: str
    is_verified: bool = False

class SignUpForm(BaseModel):
    email: EmailStr
    password: str
 
def send_verification_email(email: str, token: str):
    try:
        link = f"http://127.0.0.1:8000/verify/{token}"      
        with open('email_sender/verification_email.html', 'r') as file:
            html_content = file.read()
        html_content = html_content.replace("{{ link }}", link )    
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL  
        msg['To'] = email
        msg['Subject'] = "Email Verification"

        # Attach the HTML content to the email
        msg.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, email, msg.as_string())
            print("Verification email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
 
@app.post("/signup/")
async def signup(user: SignUpForm, background_tasks: BackgroundTasks):
    if user.email in fake_db:
        raise HTTPException(status_code=400, detail="Email already registered")
     
    fake_db[user.email] = User(email=user.email, password=user.password, is_verified=False)
     
    token = serializer.dumps(user.email, salt="email-confirm")
     
    background_tasks.add_task(send_verification_email, user.email, token)
    
    return {"message": "Sign-up successful! Please check your email to verify your account."}

@app.get("/verify/{token}")
async def verify_email(token: str):
    try:
        email = serializer.loads(token, salt="email-confirm", max_age=1200)  # 20 minutes expiry
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="The confirmation link has expired.")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid confirmation token.")
    
    if email not in fake_db:
        raise HTTPException(status_code=400, detail="User not found.")

    user = fake_db[email]
    user.is_verified = True
    fake_db[email] = user

    return {"message": "Email verified successfully! You can now log in."}




@app.post("/signin/")
async def signin(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username
    password = form_data.password

    if email not in fake_db:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    user = fake_db[email]

    if not user.is_verified:
        raise HTTPException(status_code=400, detail="Email is not verified")

    if user.password != password:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"message": "Sign-in successful!"} 









 