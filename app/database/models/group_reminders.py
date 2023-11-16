from sqlalchemy import Column, Integer, String

from app.database.models.base import Base


class GroupReminders(Base):
    __tablename__ = "GroupReminders"

    ReminderID = Column(Integer, primary_key=True, autoincrement=True)
    AuthorID = Column(Integer)
    RemindDate = Column(String)
    CreationDate = Column(String)
    ChannelID = Column(Integer)
    Message = Column(String)
    SignupMessageID = Column(Integer)
