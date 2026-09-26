# from fastapi import FastAPI, Path, Query, HTTPException
# from app.schema.book import BookRequest
# from starlette import status



# app = FastAPI()

# class Book: 
#     int: int
#     title: int 
#     author: str
#     description: str
#     rating: int
#     published_date: int


#     def __init__(self, id, title, author, description, rating, published_date):
#             self.id = id
#             self.title = title
#             self.author = author
#             self.description = description
#             self.rating = rating
#             self.published_date = published_date



# # BOOKS =[]
# BOOKS = [
#     Book(1,'computer', 'someone','very nice book ',5 ,2026),
#     Book(2,'math', 'someone','very hard book ',2 ,2023),
#     Book(3,'science', 'someone','very nice book ',5 ,2026),
#     Book(4,'history', 'someone','very intresting book ',5 ,2023),
#     Book(5,'art', 'someone','fantastic book ',8 ,2022),
#     Book(6 ,'sport', 'someone','fantastic book ',9 ,2025),
# ]


# @app.get("/books",status_code=status.HTTP_200_OK)
# async def reed_all_books():
#     return BOOKS


# @app.get('/book/{book_id}',status_code=status.HTTP_200_OK)
# async def reed_book(book_id: int = Path(gt=0)):
#     for book in BOOKS:
#           if book.id == book_id:
#                return book 
#     raise HTTPException(status_code=404, detail='Item not found')


# @app.get('/books/', status_code=status.HTTP_200_OK)
# async def read_book_by_rating(book_rating: int = Query(gt=1999,lt=2031)):
#     books_to_return = []
#     for book in BOOKS:  
#          if book.rating == book_rating:
#             books_to_return.append(book)
#     return books_to_return


# @app.get('/books/pubish')
# async def read_book_by_publish_date(published_date: int):
#     books_to_return = []
#     for book in BOOKS:  
#          if book.published_date == published_date:
#             books_to_return.append(book)
#     return books_to_return



# @app.post("/create_book",status_code=status.HTTP_201_CREATED)
# async def create_book(book_request: BookRequest):
#      new_book = Book(**book_request.dict()) #  convert the request to Book object
#      BOOKS.append(find_book_id(new_book))



# def find_book_id(book: Book):
#     book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
#     # if len(BOOKS) > 0:
#     #       book.id = BOOKS[-1].id + 1
#     # else: 
#     #       book.id = 1
#     return book 


# @app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
# async def update_book(book: BookRequest):
#      book_change = False
#      for i in range(len(BOOKS)):
#         if BOOKS[i].id == book.id:
#                BOOKS[i] = book
#                book_change = True
#      if not book_change:
#             raise HTTPException(status_code=404, detail='Item not found')



# @app.delete("/book/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
# async def delete_book(book_id: int):
#      book_change = False
#      for i in range(len(BOOKS)):
#         if BOOKS[i].id == book_id:
#             BOOKS.pop(i)
#             book_change = True
#             break
#         if not book_change:
#              raise HTTPException(status_code=404, detail='item not found')
             



from fastapi import FastAPI
from app import models
from app.database import engine
from app.router import auth, todos, admin, users

app = FastAPI()

@app.get("/health")
def health_check():
    return {'status':'Healthy'}



models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
