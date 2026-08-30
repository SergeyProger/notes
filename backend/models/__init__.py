# backend/models/__init__.py
from .note import Note
# As the project grows, add new models here:
# from .user import User
# from .referral import Referral

# Collect all documents into a single list
document_models = [
    Note,
    # User,
    # Referral,
]