from sqlalchemy import Boolean, Column, Integer, String

from app.database.models.base import Base


class Reminders(Base):
    __tablename__ = "Reminders"

    ReminderID = Column(Integer, primary_key=True, autoincrement=True)
    AuthorID = Column(Integer)
    RemindDate = Column(String)
    CreationDate = Column(String)
    ChannelID = Column(Integer)
    Message = Column(String)
    SendDirectMessage = Column(Boolean, default=False)
