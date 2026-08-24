from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
from typing import List
from pydantic import BaseModel, field_validator
from beanie import PydanticObjectId
from typing import Optional

from models import Note

import bleach # Для очистки HTML и предотвращения XSS атак

router = APIRouter(prefix="/notes", tags=["Notes"])

QUILL_ALLOWED_TAGS = ['p', 'strong', 'em', 'u', 'ol', 'ul', 'li', 'br', 'span','data-list']
QUILL_ALLOWED_ATTRS = {
    '*': ['class'],            # Разрешаем атрибут 'class' для любых тегов (Quill использует классы ql-align-*, ql-indent-*)
    'li': ['data-list'],       # Разрешаем 'data-list' специально для элементов списка
    'ol': ['data-list'],
    'ul': ['data-list'],
    'span': ['contenteditable']
}

class NoteUpdate(BaseModel):
    text: str

    @field_validator('text')
    @classmethod
    def sanitize_html(cls, value: str) -> str:
        return bleach.clean(
            value,
            tags=QUILL_ALLOWED_TAGS,
            attributes=QUILL_ALLOWED_ATTRS,
            strip=True
        )

class NoteResponse(BaseModel):
    id: PydanticObjectId  # Требуем, чтобы это была строка
    text: str
    created_at: datetime
    updated_at: datetime

class NoteListResponse(BaseModel):
    notes: List[NoteResponse]
    status: str

# index
@router.get("/", response_model=NoteListResponse)
async def get_all_notes(search: Optional[str] = Query(None)):
    """Получить все заметки, отсортированные по дате создания (новые первыми)"""
    query = Note.find({"$text": {"$search": search}}) if search and search.strip() else Note.find_all()
    notes = await query.sort("-created_at").to_list()
    return {"notes": notes, "status": "success"}

# show
@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(note_id: str):
    """Получить одну заметку по ID"""
    try:
        note_obj_id = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid note ID")

    note = await Note.get(note_obj_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note

# create
@router.post("/")
async def create_note(data: NoteUpdate):
    """Создать новую заметку"""
    new_note = Note(text=data.text)
    await new_note.insert()

    return {
        "message": f"Note '{data.text}' has been created",
        "id": str(new_note.id),
        "status": "success"
    }

# update
@router.put("/{note_id}")
async def update_note(note_id: str, data: NoteUpdate):
    """Обновить заметку по ID"""

    print(f"Received update request for note ID: {note_id} with data: {data}")
    try:
        note_obj_id = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid note ID")

    note = await Note.get(note_obj_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.text = data.text

    await note.save()

    print(f"Note with ID {note_id} updated successfully. New text: {note.text}")

    return {
        "message": "Note updated successfully",
        "id": note_id,
        "status": "success"
    }

# delete
@router.delete("/{note_id}")
async def delete_note(note_id: str):
    """Удалить заметку по ID"""
    try:
        note_obj_id = ObjectId(note_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid note ID")

    note = await Note.get(note_obj_id)

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await note.delete()

    return {
        "message": "Note deleted successfully",
        "id": note_id,
        "status": "success"
    }
