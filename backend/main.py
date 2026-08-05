""" Purpose:
Start FastAPI app
register API routes

Responsibility:
Initialize application
Connect routers
Start server

---> You will import the auth routes here. """


from fastapi import FastAPI
from app.db.session import initialize_database

app = FastAPI()


@app.on_event("startup")
def startup():
    initialize_database()


@app.get("/")
def home():
    return {"message": "Campus Lost & Found API Running"}