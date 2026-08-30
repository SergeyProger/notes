from pydantic import BaseModel, Field
from datetime import datetime
from beanie import before_event, Replace, SaveChanges, Update

class TimestampMixin(BaseModel):
    """
    Mixin for adding timestamps.
    Any model that inherits this class automatically gets these fields.
    """
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @before_event(Replace, SaveChanges, Update)
    def update_timestamp(self):
        """
        Equivalent of before_update / before_save.
        Updates the updated_at field right before writing to the DB.
        """
        self.updated_at = datetime.utcnow()