# AI-Agent-Anarix

AI-Agent-Anarix is an AI-powered E-commerce analytics assistant. It allows users to ask natural language questions about their e-commerce data and receive insightful answers powered by a Large Language Model (LLM). The project features a FastAPI backend, a modern JavaScript frontend, and integration with Google Gemini for LLM capabilities.

---

## Features

- **Conversational Analytics:** Ask questions about your e-commerce data in plain English.
- **LLM-Powered:** Uses Google Gemini to generate SQL queries and human-readable answers.
- **Interactive Chat UI:** Clean, responsive frontend for seamless user experience.
- **Streaming Responses:** Answers are streamed in real-time for a chat-like feel.

---

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy, Google Generative AI (Gemini), SQLite
- **Frontend:** HTML, CSS, JavaScript (Vanilla)
- **Other:** dotenv for environment variables, CORS middleware

---

## Project Structure

```
.
├── backend
│   ├── app
│   │   ├── api
│   │   │   ├── v1
│   │   │   │   ├── endpoints
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   ├── core
│   │   │   ├── config.py
│   │   │   └── __init__.py
│   │   ├── db
│   │   │   ├── base_class.py
│   │   │   ├── session.py
│   │   │   └── __init__.py
│   │   ├── models
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   ├── schemas
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   ├── services
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   └── main.py
│   ├── alembic
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   │       └── README
│   ├── requirements.txt
│   └── README.md
└── frontend
    ├── index.html
    ├── script.js
    ├── style.css
    └── README.md
```

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AI-Agent-Anarix.git
   cd AI-Agent-Anarix
   ```
2. Set up the backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. Set up the frontend:
   ```bash
   cd frontend
   # No dependencies, just open index.html in a browser
   ```
4. Configure environment variables:
   - Copy `.env.example` to `.env` in the `backend` directory and update the values as needed.

---

## Usage

1. Start the backend server:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
2. Open the frontend:
   - Open `frontend/index.html` in a web browser.

---

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Create a new Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Inspired by the need for intelligent data analysis tools
- Powered by Google Gemini for advanced LLM capabilities
- Built with passion by the Anarix team