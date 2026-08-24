import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime
from typing import Optional

app = FastAPI()

# Настройка CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NoteUpdate(BaseModel):
    text: str

# Инициализация подключения к БД
# Берем адрес из переменных окружения (задано в docker-compose.yml)
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
db = client.app_database     # Наша база данных
collection = db.texts        # Наша коллекция (аналог таблицы)


@app.get("/")
async def root():
    """Главный маршрут - возвращает все заметки"""
    return await get_all_notes()


@app.post("/write")
async def write_text(data: NoteUpdate):
    """Создать новую заметку"""
    new_document = {
        "text": data.text,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    result = await collection.insert_one(new_document)

    return {
        "message": f"Text '{data.text}' has been written to MongoDB",
        "id": str(result.inserted_id),
        "status": "success"
    }


@app.get("/notes")
async def get_all_notes():
    """Получить все заметки, отсортированные по дате создания (новые первыми)"""
    notes = []
    cursor = collection.find({}).sort("created_at", -1)
    
    async for doc in cursor:
        notes.append({
            "id": str(doc["_id"]),
            "text": doc.get("text", ""),
            "created_at": doc.get("created_at", ""),
            "updated_at": doc.get("updated_at", "")
        })
    
    return {"notes": notes, "status": "success"}


@app.get("/notes/{note_id}")
async def get_note(note_id: str):
    """Получить одну заметку по ID"""
    try:
        note_obj_id = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid note ID")
    
    note = await collection.find_one({"_id": note_obj_id})
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return {
        "id": str(note["_id"]),
        "text": note.get("text", ""),
        "created_at": note.get("created_at", ""),
        "updated_at": note.get("updated_at", ""),
        "status": "success"
    }


@app.put("/notes/{note_id}")
async def update_note(note_id: str, data: NoteUpdate):
    """Обновить заметку по ID"""
    try:
        note_obj_id = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid note ID")
    
    result = await collection.update_one(
        {"_id": note_obj_id},
        {
            "$set": {
                "text": data.text,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return {
        "message": "Note updated successfully",
        "id": note_id,
        "status": "success"
    }


@app.delete("/notes/{note_id}")
async def delete_note(note_id: str):
    """Удалить заметку по ID"""
    try:
        note_obj_id = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid note ID")
    
    result = await collection.delete_one({"_id": note_obj_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return {
        "message": "Note deleted successfully",
        "id": note_id,
        "status": "success"
    }