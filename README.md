🚀 Library Management System (FastAPI + Streamlit)

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
