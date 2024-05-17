from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as record_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


class App:
    ...


app = FastAPI()


if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.3.54", port=8000, log_level="info")

config = dotenv_values(".env")


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["DB_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(record_router, tags=["records"], prefix="/records")
