
# 📚 Library Assistant API

An intelligent, API-powered library system that lets users and books be managed, borrowed, and queried using natural language. Built using **FastAPI**, **SQLite**, **SQLAlchemy**, and **LangChain**.

**🔗 GitHub Repository:** [swadhikar/sql_library_agent](https://github.com/swadhikar/sql_library_agent)

---

## 🚀 Features

- Add and view users and books
- Borrow books with due dates
- Natural language Q&A over the library database via OpenAI (`gpt-3.5-turbo`)
- Ready-to-use endpoints with FastAPI

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/swadhikar/sql_library_agent.git
cd sql_library_agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** Create a `.env` file in the root directory with your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_key
```

### 3. Run the App

```bash
uvicorn api_main:app --reload
```

The app will be available at `http://127.0.0.1:8000`.

---

## 📘 API Endpoints

### ➕ Add User
```http
POST /users/?name=swadhi
```

### ➕ Add Book
```http
POST /books/?title=1984
```

### 📖 Borrow Book
```http
POST /borrow/?username=swadhi&title=1984
```

### 👥 Get All Users
```http
GET /users/
```

### 📚 Get All Books
```http
GET /books/
```

### ❓ Natural Language Q&A
```http
GET /question?question=What are the books swadhi borrowed?
```

📥 **Sample Response:**
```json
{
  "question": "What are the books swadhi borrowed?",
  "answer": "Swadhi borrowed the books \"english\" and \"Heart Beat 2\"."
}
```

---

## 🤖 Powered By

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [LangChain](https://www.langchain.com/)
- [OpenAI](https://openai.com/)

---

## 🧪 Development Notes

- Database: `SQLite` via `library.db`
- Natural language queries use `LangChain SQL agent` with OpenAI models
- Code is modular: `api_main.py`, `library.py`, `sql_agent.py`

---

## 📂 File Structure

```
.
├── api_main.py          # FastAPI endpoints
├── library.py           # Database models and functions
├── sql_agent.py         # LangChain SQL agent logic
├── library.db           # SQLite database (auto-generated)
└── .env                 # API keys (excluded from repo)
```

---

## 📄 License

MIT License
