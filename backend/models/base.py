from pydantic import BaseModel, Field
from datetime import datetime
from beanie import before_event, Replace, SaveChanges, Update

class TimestampMixin(BaseModel):
    """
    Примесь (Mixin) для добавления таймстемпов.
    Любая модель, которая наследует этот класс, автоматически получит эти поля.
    """
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @before_event(Replace, SaveChanges, Update)
    def update_timestamp(self):
        """
        Аналог before_update / before_save.
        Обновляет поле updated_at непосредственно перед записью в БД.
        """
        self.updated_at = datetime.utcnow()