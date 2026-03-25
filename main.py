# =========================
# 1. IMPORTS
# =========================
from fastapi import FastAPI, Query,HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

# =========================
# 2. APP INIT
# =========================
app = FastAPI()

# =========================
# 3. DATA (In-Memory)
# =========================
books = [
    {"id": 1, "title": "Python Basics", "author": "John Doe", "genre": "Tech", "is_available": True},
    {"id": 2, "title": "AI Revolution", "author": "Jane Smith", "genre": "Science", "is_available": True},
    {"id": 3, "title": "History of India", "author": "R. Kumar", "genre": "History", "is_available": False},
    {"id": 4, "title": "Machine Learning", "author": "Andrew Ng", "genre": "Tech", "is_available": True},
    {"id": 5, "title": "Fiction World", "author": "A. Writer", "genre": "Fiction", "is_available": True},
    {"id": 6, "title": "Data Science", "author": "B. Analyst", "genre": "Tech", "is_available": False},
    {"id": 7, "title": "Deep Learning Guide", "author": "Ian Goodfellow", "genre": "Tech", "is_available": True},
    {"id": 8, "title": "Space Exploration", "author": "Neil Tyson", "genre": "Science", "is_available": True},
    {"id": 9, "title": "Indian Freedom Struggle", "author": "S. Bose", "genre": "History", "is_available": False},
    {"id": 10, "title": "Advanced Python", "author": "Mark Lutz", "genre": "Tech", "is_available": True},
    {"id": 11, "title": "The Last Kingdom", "author": "B. Cornwell", "genre": "Fiction", "is_available": True},
    {"id": 12, "title": "Quantum Physics", "author": "R. Feynman", "genre": "Science", "is_available": False},
    {"id": 13, "title": "World War II", "author": "A. Roberts", "genre": "History", "is_available": True},
    {"id": 14, "title": "Data Structures", "author": "N. Wirth", "genre": "Tech", "is_available": True},
    {"id": 15, "title": "Mystery Island", "author": "J. Verne", "genre": "Fiction", "is_available": False},
    {"id": 16, "title": "AI for Everyone", "author": "Andrew Ng", "genre": "Tech", "is_available": True},
    {"id": 17, "title": "Cosmos", "author": "Carl Sagan", "genre": "Science", "is_available": True},
    {"id": 18, "title": "Ancient Civilizations", "author": "H. Wells", "genre": "History", "is_available": False},
    {"id": 19, "title": "Web Development", "author": "M. Developer", "genre": "Tech", "is_available": True},
    {"id": 20, "title": "Fantasy Land", "author": "G. Martin", "genre": "Fiction", "is_available": True},
    {"id": 21, "title": "Biology Basics", "author": "C. Darwin", "genre": "Science", "is_available": False},
    {"id": 22, "title": "Modern India", "author": "Bipan Chandra", "genre": "History", "is_available": True},
    {"id": 23, "title": "Algorithms", "author": "T. Cormen", "genre": "Tech", "is_available": True},
    {"id": 24, "title": "Horror Nights", "author": "S. King", "genre": "Fiction", "is_available": False},
    {"id": 25, "title": "Astrophysics", "author": "N. Tyson", "genre": "Science", "is_available": True},
    {"id": 26, "title": "Medieval History", "author": "J. Norwich", "genre": "History", "is_available": True}
]

borrow_records = []
record_counter = 1
queue = {}

# =========================
# 4. MODELS
# =========================
class BorrowRequest(BaseModel):
    member_name: str = Field(..., min_length=2)
    book_id: int = Field(..., gt=0)
    mobile_number: str = Field(..., min_length=10, max_length=13)
    borrow_days: int = Field(..., gt=0, le=30)
    member_id: str = Field(..., min_length=4)


class BookCreate(BaseModel):
    title: str = Field(..., min_length=2)
    author: str
    genre: str


# =========================
# 5. HELPERS
# =========================
def find_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    return None


def calculate_due_date(days: int):
    due = datetime.now() + timedelta(days=days)
    return due.strftime("%Y-%m-%d")


# =========================
# 6. ROUTES (Q1 → Q20)
# =========================

@app.get("/")
def home():
    return {"message": "Welcome to City Public Library"}


@app.get("/books")
def get_books():
    return {
        "total_books": len(books),
        "available_books": len([b for b in books if b["is_available"]]),
        "books": books
    }


@app.get("/books/summary")
def books_summary():
    return {
        "total_books": len(books),
        "available_books": len([b for b in books if b["is_available"]]),
        "unavailable_books": len([b for b in books if not b["is_available"]]),
        "currently_borrowed": len([r for r in borrow_records if r["status"] == "borrowed"]),
        "total_borrow_transactions": len(borrow_records),
        "total_returned": len([r for r in borrow_records if r["status"] == "returned"])
    }


@app.get("/books/filter")
def filter_books(genre: str = Query(None), is_available: bool = Query(None)):
    result = books

    if genre:
        result = [b for b in result if b["genre"].lower() == genre.lower()]

    if is_available is not None:
        result = [b for b in result if b["is_available"] == is_available]

    return {"count": len(result), "books": result}


@app.get("/books/search")
def search_books(keyword: str = Query(None)):
    if not keyword or keyword.strip() == "":
        return {"message": "Please provide a keyword"}

    result = [b for b in books if keyword.lower() in b["title"].lower()]
    return {"count": len(result), "books": result}


@app.get("/books/sort")
def sort_books(order: str = "asc"):
    return {"books": sorted(books, key=lambda x: x["title"], reverse=(order == "desc"))}


@app.get("/books/page")
def paginate_books(skip: int = 0, limit: int = 5):
    return {"books": books[skip: skip + limit]}


@app.get("/books/browse")
def browse_books(keyword: str = Query(None), skip: int = 0, limit: int = 5):
    result = books

    if keyword:
        result = [b for b in result if keyword.lower() in b["title"].lower()]

    return {"count": len(result), "books": result[skip: skip + limit]}


@app.get("/books/{book_id}")
def get_book(book_id: int):
    book = find_book(book_id)
    return book if book else {"error": "Book not found"}


@app.get("/borrow-records")
def get_records():
    return {"total_records": len(borrow_records), "records": borrow_records}


@app.get("/borrow-records/search")
def search_records(member_name: str = Query(None), skip: int = 0, limit: int = 5):
    result = borrow_records

    if member_name:
        result = [r for r in result if member_name.lower() in r["member_name"].lower()]

    return {"count": len(result), "records": result[skip: skip + limit]}


# =========================
# BORROW
# =========================
@app.post("/borrow")
def borrow_book(request: BorrowRequest):
    global record_counter

    book = find_book(request.book_id)
    if not book:
        return {"error": "Book not found"}

    if not book["is_available"]:
        queue.setdefault(request.book_id, []).append({
            "member_name": request.member_name,
            "member_id": request.member_id,
            "mobile_number": request.mobile_number
        })
        return {
            "message": "Book not available, added to queue",
            "queue_position": len(queue[request.book_id])
        }

    book["is_available"] = False

    record = {
        "record_id": record_counter,
        "member_name": request.member_name,
        "member_id": request.member_id,
        "book_id": request.book_id,
        "mobile_number": request.mobile_number,
        "borrow_days": request.borrow_days,
        "borrow_date": datetime.now().strftime("%Y-%m-%d"),
        "due_date": calculate_due_date(request.borrow_days),
        "return_date": None,
        "status": "borrowed",
        "is_premium": request.borrow_days > 14
    }

    borrow_records.append(record)
    record_counter += 1

    return {"message": "Book borrowed successfully", "record": record}


# =========================
# ✅ FIXED RETURN (record_id)
# =========================
@app.post("/return/{record_id}")
def return_book(record_id: int):

    record = next((r for r in borrow_records if r["record_id"] == record_id), None)

    if not record:
        return {"error": "Record not found"}

    if record["status"] == "returned":
        return {"message": "Already returned"}

    # Update record
    record["status"] = "returned"
    record["return_date"] = datetime.now().strftime("%Y-%m-%d")

    book = find_book(record["book_id"])

    # Queue handling
    if record["book_id"] in queue and queue[record["book_id"]]:
        next_user = queue[record["book_id"]].pop(0)
        return {"message": "Book assigned to next user", "assigned_to": next_user}

    book["is_available"] = True
    return {"message": "Book returned successfully"}


# =========================
# CRUD
# =========================
@app.post("/books")
def add_book(book: BookCreate):

    for existing_book in books:
        if (
            existing_book["title"].strip().lower() == book.title.strip().lower() and
            existing_book["author"].strip().lower() == book.author.strip().lower() and
            existing_book["genre"].strip().lower() == book.genre.strip().lower()
        ):
            raise HTTPException(
                status_code=400,
                detail="Book already exists"
            )

    new_book = {
        "id": len(books) + 1,
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "is_available": True
    }

    books.append(new_book)

    return {"message": "Book added successfully", "book": new_book}


@app.put("/books/{book_id}")
def update_book(book_id: int, updated: BookCreate):
    book = find_book(book_id)
    if not book:
        return {"error": "Book not found"}

    book.update(updated.dict())
    return {"message": "Book updated successfully", "book": book}


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    book = find_book(book_id)
    if not book:
        return {"error": "Book not found"}

    books.remove(book)
    return {"message": "Book deleted successfully"}