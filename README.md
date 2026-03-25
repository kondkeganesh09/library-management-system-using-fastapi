🚀 Library Management System (FastAPI + Streamlit)
Project Highlights
- Designed a real-world backend system using FastAPI
- Implemented queue-based book allocation system
- Built complete borrow-return workflow with state management
- Integrated backend APIs with a Streamlit UI
- Applied validation and error handling for robust API design

📌 Overview
This project is a backend-driven Library Management System built using FastAPI with a Streamlit UI.
It supports real-world workflows like book borrowing, queue management, and return handling.

⚙️ Tech Stack
- FastAPI
- Python
- Streamlit
- Pydantic
- Uvicorn

🔧 Features
- REST APIs (GET, POST, PUT, DELETE)
- Data validation using Pydantic
- Book borrowing system with due date calculation
- Queue system for unavailable books
- Automatic assignment on return
- Search, filtering, sorting & pagination
- Borrow & return tracking system
- Interactive UI using Streamlit

▶️ How to Run
```bash
pip install -r requirements.txt
uvicorn main:app --reload
streamlit run app.py

📡 API Endpoints
| Method | Endpoint | Description |
|-------|--------|------------|
| GET | /books | Get all books |
| GET | /books/search | Search books |
| POST | /borrow | Borrow a book |
| POST | /return/{id} | Return a book |
| POST | /books | Add new book |
| PUT | /books/{id} | Update book |
| DELETE | /books/{id} | Delete book |

🔄 System Workflow

1. User searches or browses books  
2. User borrows a book  
3. If unavailable → added to queue  
4. Book return updates record  
5. Next user in queue gets access automatically  
