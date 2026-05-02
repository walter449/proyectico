from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import students, auth
from database import engine, Base
from models import user_db_model

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(students.router)
app.include_router(auth.router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
