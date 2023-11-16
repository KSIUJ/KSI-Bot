from sqlalchemy import Column, Integer, String

from app.database.models.base import Base


class Reminders(Base):
    __tablename__ = "Reminders"

    ReminderID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(String)
    RemindDate = Column(String)
    ChannelID = Column(String)
    Message = Column(String)
