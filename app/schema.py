from typing import Optional
from pydantic import BaseModel, Field



# class BookRequest(BaseModel):
#     id: Optional[int] =Field(description="ID is not needes on create", default=None)
#     title: str = Field(min_length=1)
#     author: str = Field(min_length=3)
#     description: str = Field(min_length=1, max_length=100)
#     rating: int = Field(gt=0, lt=6)
#     published_date: int = Field(gt=1999,ls=2031)


#     # model_config = {}

#     class Config: 
#         schema_extra = {
#             'example' : {
#                 'title': 'A new book',
#                 'author': 'conding',
#                 'description': 'something about book',
#                 'rating': 5,
#                 'published_date': 2029
#             }
#         }



class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3 , max_length=100)
    priority: int = Field(gt=0)
    complete: bool