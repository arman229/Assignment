from fastapi import FastAPI
from email_sender.db_connections import lifespan 
from email_sender.routes.user import router
from email_sender.routes.admin import adminrouter


app :FastAPI= FastAPI(lifespan=lifespan, title="User services ") 




@app.get('/welcome')
def welcome():
    return {"message": "Welcome to the User service"}

app.include_router(router)
app.include_router(adminrouter)

 