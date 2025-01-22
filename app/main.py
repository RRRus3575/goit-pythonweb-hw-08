from fastapi import FastAPI
from .models import Base
from .database import engine
from .routers import contacts

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(contacts.router, prefix="/contacts", tags=["Contacts"])
