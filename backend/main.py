""" Purpose:
Start FastAPI app
register API routes

Responsibility:
Initialize application
Connect routers
Start server

---> You will import the auth routes here. """


from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.db.session import initialize_database

app = FastAPI(title="Campus Lost & Found API")


@app.on_event("startup")
def startup():
    initialize_database()

app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "Campus Lost & Found API Running"}