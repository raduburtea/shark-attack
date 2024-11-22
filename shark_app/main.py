import uvicorn
from dotenv import dotenv_values
from fastapi import FastAPI
from pymongo import MongoClient
from routes.api import router as api_router

config = dotenv_values(".env")

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient("mongodb://0.0.0.0:27017/")
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Project connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
