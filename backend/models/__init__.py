# backend/models/__init__.py
from .note import Note
# По мере роста проекта добавляете сюда новые модели:
# from .user import User
# from .referral import Referral

# Собираем все документы в один список
document_models = [
    Note,
    # User,
    # Referral,
]