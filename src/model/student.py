from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.base.db import Base

class Student(Base):
    __tablename__ = "students"
    

    id = Column(Integer , primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    last_name = Column(String , nullable=True)
    first_name = Column(String , nullable=True)
    
    user = relationship("User" , back_populates="student")