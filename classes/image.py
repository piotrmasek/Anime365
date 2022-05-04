from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


class Image(declarative_base()):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    file_name = Column(String(128), nullable=False)
    timestamp = Column(Integer, nullable=False, index=True)
    anime = Column(String(256))
    difficulty = Column(Integer)

    def __str__(self) -> str:
        return f"id: {self.id}, file: {self.file_name}, date: {self.timestamp}, anime: {self.anime}," \
               f" diff: {self.difficulty}"
