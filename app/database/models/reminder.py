from sqlalchemy import Column, Integer, String, Boolean

from app.database.models.base import Base


class Reminders(Base):
    __tablename__ = "Reminders"

    ReminderID = Column(Integer, primary_key=True, autoincrement=True)
    AuthorID = Column(String)
    RemindDate = Column(String)
    CreationDate = Column(String)
    ChannelID = Column(String)
    Message = Column(String)
    SendDirectMessage = Column(Boolean, default=False)
