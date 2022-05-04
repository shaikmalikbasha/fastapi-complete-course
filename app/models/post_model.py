from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")
    # def to_json(self):
    #     return {
    #         "_id": self.id,
    #         "title": self.title,
    #         "content": self.content,
    #         "is_published": self.is_published,
    #         "created_at": self.created_at,
    #     }
