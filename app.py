import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="📚 Library Pro", layout="wide")

# =========================
# 🎨 UPDATED THEME
# =========================
st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

/* HOME */
.home-bg {
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                url("https://images.unsplash.com/photo-1524995997946-a1c2e315a42f");
    background-size: cover;
    background-position: center;
    padding: 100px;
    border-radius: 15px;
    color: white;
    text-align: center;
}

/* METRIC CARD */
.metric-card {
    border-radius: 16px;
    padding: 22px;
    margin: 10px;
    text-align: center;
    color: white;
    font-weight: 600;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

/* COLORS */
.total-books { background: linear-gradient(135deg, #6366f1, #4f46e5); }
.available-books { background: linear-gradient(135deg, #10b981, #059669); }
.unavailable-books { background: linear-gradient(135deg, #ef4444, #dc2626); }
.total-records { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }
.active-records { background: linear-gradient(135deg, #f59e0b, #d97706); }

/* CARD */
.card {
    border-radius: 14px;
    padding: 18px;
    margin: 10px;
    background: white;
    box-shadow: 0 6px 15px rgba(0,0,0,0.08);
    color: #1f2937;
}

.available { border-left: 6px solid #10b981; }
.unavailable { border-left: 6px solid #ef4444; }
.borrowed { border-left: 6px solid #f59e0b; }
.returned { border-left: 6px solid #3b82f6; }

.title { font-size: 18px; font-weight: bold; color:#111827; }
.meta { font-size: 14px; color:#4b5563; }

.badge {
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: bold;
}

.green { background:#ecfdf5; color:#065f46; }
.red { background:#fef2f2; color:#7f1d1d; }
.orange { background:#fffbeb; color:#92400e; }
.blue { background:#eff6ff; color:#1e3a8a; }

</style>
""", unsafe_allow_html=True)

# =========================
# METRIC CARD
# =========================
def metric_card(title, value, css_class):
    return f"""
    <div class="metric-card {css_class}">
        <div>{title}</div>
        <div style="font-size:30px;font-weight:bold;">{value}</div>
    </div>
    """

# =========================
# BOOK CARD
# =========================
def show_books(books):
    cols = st.columns(3)
    for i, b in enumerate(books):
        col = cols[i % 3]

        cls = "available" if b["is_available"] else "unavailable"
        badge = "green" if b["is_available"] else "red"
        status = "Available" if b["is_available"] else "Not Available"

        col.markdown(f"""
        <div class="card {cls}">
            <div class="title">{b['title']}</div>
            <div class="meta">👤 {b['author']}</div>
            <div class="meta">📚 {b['genre']}</div><br>
            <span class="badge {badge}">{status}</span><br><br>
            <small>Book ID: {b['id']}</small>
        </div>
        """, unsafe_allow_html=True)

# =========================
# RECORD CARD
# =========================
def show_records(records):
    cols = st.columns(2)
    for i, r in enumerate(records):
        col = cols[i % 2]

        cls = "borrowed" if r["status"] == "borrowed" else "returned"
        badge = "orange" if r["status"] == "borrowed" else "blue"

        with col:
            st.markdown(f"""
            <div class="card {cls}">
                <div class="title">📘 Book ID: {r['book_id']}</div>
                <div class="meta">👤 {r['member_name']}</div>
                <div class="meta">🆔 {r['member_id']}</div>
                <div class="meta">📱 {r.get('mobile_number', 'N/A')}</div>
                <div class="meta">📅 Borrow: {r['borrow_date']}</div>
                <div class="meta">⏳ Due: {r['due_date']}</div>
                <div class="meta">🔄 Return: {r['return_date']}</div><br>
                <span class="badge {badge}">{r['status'].upper()}</span>
                <br><br>
                <small>Record ID: {r['record_id']}</small>
            </div>
            """, unsafe_allow_html=True)

            if r["status"] == "borrowed":
                if st.button("Return Book", key=f"return_{r['record_id']}"):
                    res = requests.post(f"{API_URL}/return/{r['record_id']}")
                    st.success(res.json())
                    st.rerun()

# =========================
# BORROW RESULT CARD
# =========================
def show_borrow_card(data):
    if "record" not in data:
        st.warning(data.get("message", "Something went wrong"))
        return

    r = data["record"]

    st.markdown(f"""
    <div class="card borrowed">
        <div class="title">✅ Book Borrowed Successfully</div>
        <div class="meta">📘 Book ID: {r['book_id']}</div>
        <div class="meta">👤 Name: {r['member_name']}</div>
        <div class="meta">🆔 Member ID: {r['member_id']}</div>
        <div class="meta">📞 Mobile: {r.get('mobile_number', 'N/A')}</div>
        <div class="meta">📅 Borrow: {r['borrow_date']}</div>
        <div class="meta">⏳ Due: {r['due_date']}</div><br>
        <span class="badge orange">BORROWED</span>
    </div>
    """, unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
menu = st.sidebar.radio("📚 Menu", [
    "Home", "View Books", "Search & Filter",
    "Borrow Book", "Return Book",
    "Add Book", "Update Book","Delete Book", "Records"
])

# =========================
# HOME
# =========================
if menu == "Home":
    st.markdown("""
    <div class="home-bg">
        <h1>📚 City Public Library</h1>
        <p>Welcome to your smart digital library system</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# VIEW BOOKS
# =========================
elif menu == "View Books":
    data = requests.get(f"{API_URL}/books").json()

    total = data["total_books"]
    available = data["available_books"]
    unavailable = total - available

    col1, col2, col3 = st.columns(3)
    col1.markdown(metric_card("Total Books", total, "total-books"), True)
    col2.markdown(metric_card("Available", available, "available-books"), True)
    col3.markdown(metric_card("Unavailable", unavailable, "unavailable-books"), True)

    show_books(data["books"])

# =========================
# 🔥 ONLY CHANGE HERE (SEARCH + GENRE)
# =========================
elif menu == "Search & Filter":
    keyword = st.text_input("Search Title")

    # Fetch books to extract genres
    all_books = requests.get(f"{API_URL}/books").json()["books"]
    genres = list(set([b["genre"] for b in all_books]))

    selected_genre = st.selectbox("Filter by Genre", ["All"] + genres)

    if st.button("Search"):

        # ✅ VALIDATION
        if not keyword.strip():
            st.error("❌ Please fill complete details")
        else:
            res = requests.get(
                f"{API_URL}/books/search",
                params={"keyword": keyword}
            ).json()

            books_data = res["books"]

            # ✅ APPLY GENRE FILTER ONLY IF NOT "All"
            if selected_genre != "All":
                books_data = [b for b in books_data if b["genre"] == selected_genre]

            # ✅ FINAL CHECK
            if not books_data:
                st.error("❌ No book like this in collection. Please check spelling or try another keyword.")
            else:
                show_books(books_data)

# =========================
# BORROW
# =========================
elif menu == "Borrow Book":
    with st.form("borrow_form"):
        name = st.text_input("Member Name")
        member_id = st.text_input("Member ID")

        # ✅ Country Code + Mobile
        col1, col2 = st.columns([1, 3])
        with col1:
            country_code = st.text_input("Code", value="+91")
        with col2:
            mobile_number = st.text_input("Mobile Number")

        book_id = st.number_input("Book ID", min_value=1)
        days = st.slider("Days", 1, 30)

        submit = st.form_submit_button("Borrow")

        if submit:
            # ✅ Validation
            if not name or not member_id or not mobile_number:
                st.error("❌ Please fill all fields")
            else:
                full_mobile = f"{country_code}{mobile_number}"

                res = requests.post(f"{API_URL}/borrow", json={
                    "member_name": name,
                    "member_id": member_id,
                    "mobile_number": full_mobile,
                    "book_id": int(book_id),
                    "borrow_days": int(days)
                })

                # ✅ ERROR DEBUGGING
                if res.status_code != 200:
                    st.error(f"❌ Error: {res.text}")
                else:
                    show_borrow_card(res.json())

# =========================
# RETURN
# =========================
elif menu == "Return Book":
    search = st.text_input("Search Member Name / ID")

    if search:
        records = requests.get(f"{API_URL}/borrow-records").json()["records"]

        filtered = [
            r for r in records
            if search.lower() in r["member_name"].lower()
            or search.lower() in r["member_id"].lower()
        ]

        if not filtered:
            st.warning("❌ No book borrowed by this user")
        else:
            show_records(filtered)

# =========================
# ADD BOOK
# =========================
elif menu == "Add Book":
    with st.form("add"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        genre = st.text_input("Genre")

        if st.form_submit_button("Add"):
            res = requests.post(f"{API_URL}/books", json={
                "title": title,
                "author": author,
                "genre": genre
            })

            data = res.json()

            if res.status_code == 200:
                st.success(data["message"])
            else:
                st.error(f"❌ {data.get('detail')}")
# =========================
# UPDATE BOOK
# =========================
elif menu == "Update Book":
    book_id = st.number_input("Book ID", 1)
    title = st.text_input("New Title")
    author = st.text_input("New Author")
    genre = st.text_input("New Genre")

    if st.button("Update"):
        res = requests.put(f"{API_URL}/books/{book_id}", json={
            "title": title,
            "author": author,
            "genre": genre
        })
        st.success(res.json())

#=========================================
#Delete book
#================================================
elif menu == "Delete Book":
    st.subheader("🗑️ Delete Book")

    book_id = st.number_input("Enter Book ID to Delete", min_value=1)

    if st.button("Delete Book"):
        res = requests.delete(f"{API_URL}/books/{book_id}")

        # ✅ Show proper response
        if res.status_code == 200:
            st.success("✅ Book deleted successfully")
        else:
            st.error(f"❌ Error: {res.text}")
# =========================
# RECORDS
# =========================
elif menu == "Records":
    data = requests.get(f"{API_URL}/borrow-records").json()
    records = data["records"]

    total = len(records)
    active = len([r for r in records if r["status"] == "borrowed"])

    col1, col2 = st.columns(2)
    col1.markdown(metric_card("Total Records", total, "total-records"), True)
    col2.markdown(metric_card("Active Borrowed", active, "active-records"), True)

    show_records(records)