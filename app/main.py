from fastapi import FastAPI
from app.routers import orders

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "My e-commerce app"}


app.include_router(orders.router)