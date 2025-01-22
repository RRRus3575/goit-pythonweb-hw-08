from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from ..database import get_db
from ..schemas import ContactCreate, ContactResponse, ContactUpdate
from ..crud import create_contact, get_contacts, get_contact_by_id, update_contact, delete_contact, search_contacts, get_upcoming_birthdays

router = APIRouter()

@router.post("/", response_model=ContactResponse)
async def create(contact: ContactCreate, db: AsyncSession = Depends(get_db)):
    return await create_contact(db, contact)

@router.get("/", response_model=List[ContactResponse])
async def read_all(db: AsyncSession = Depends(get_db)):
    return await get_contacts(db)

@router.get("/{contact_id}", response_model=ContactResponse)
async def read_one(contact_id: int, db: AsyncSession = Depends(get_db)):
    contact = await get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.get("/search/", response_model=List[ContactResponse])
async def search(query: str, db: AsyncSession = Depends(get_db)):
    return await search_contacts(db, query)


@router.put("/{contact_id}", response_model=ContactResponse)
async def update(contact_id: int, contact: ContactUpdate, db: AsyncSession = Depends(get_db)):
    updated_contact = await update_contact(db, contact_id, contact)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact

@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete(contact_id: int, db: AsyncSession = Depends(get_db)):
    deleted_contact = await delete_contact(db, contact_id)
    if not deleted_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return deleted_contact

@router.get("/birthdays/", response_model=List[ContactResponse])
async def upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    return await get_upcoming_birthdays(db)