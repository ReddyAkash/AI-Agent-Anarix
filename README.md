# E-commerce AI Agent 🤖

An advanced AI-powered chatbot designed to answer questions about e-commerce data. It provides a user-friendly chat interface where users can ask questions in natural language, and the agent understands the user's intent, queries a database, and returns answers in a human-readable format.

The agent is built with a sophisticated backend using Python, FastAPI, and Google's Gemini LLM, and a sleek, responsive frontend using HTML and Tailwind CSS.

---

## ✨ Key Features

* **Natural Language to SQL:** Translates complex user questions like "What was my total revenue last month?" into precise SQL queries.
* **Conversational AI:** Engages in general conversation, recognizing when a question does not require database access (e.g., "Hello", "How are you?").
* **Real-time Streaming:** Answers are streamed back to the user, creating an friendly interactive session between user and chatbot.
* **Self-Contained Web Application:** The FastAPI backend serves the frontend, allowing the entire project to be run from a single command.

---

## 📁 Project Structure

The repository is organized into two main parts: `backend` and `frontend`.

```
e-commerce-ai-agent/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── llm_helper.py
│   │   └── database_setup.py
│   │
│   ├── data/
│   │   ├── ad_sales.csv
│   │   ├── total_sales.csv
│   │   └── eligibility.csv
│   │
│   ├── .env
│   ├── .gitignore
│   ├── requirements.txt
│   └── run.py
│
└── frontend/
    └── index.html
```

---

## ⚙️ Code File Functionality

### Backend

* **`run.py`**: The entry point of the application. It runs `database_setup.py` to ensure the database is ready and then starts the Uvicorn server for the FastAPI app.
* **`app/main.py`**: The heart of the backend. It initializes FastAPI, serves the `index.html` frontend, and defines the crucial `/ask` API endpoint. It contains the hybrid logic to decide between a hardcoded query, an LLM-generated query, a general conversation, or a chart visualization.
* **`app/llm_helper.py`**: Contains all helper functions that interact with external services. This includes `get_sql_query()`, `get_general_response()`, `execute_sql_query()`, and `generate_chart_image()`.
* **`app/database_setup.py`**: A utility script that reads CSV files from the `/data` directory and loads them into a SQLite database (`ecommerce_data.db`).
* **`requirements.txt`**: Defines the Python libraries needed for the project.
* **`.env`**: A crucial security file (not committed to Git) where you store your `GEMINI_API_KEY`.
* **`.gitignore`**: Prevents sensitive files (`.env`, `.db`) and clutter (`__pycache__`) from being committed to Git.

### Frontend

* **`index.html`**: A single, self-contained HTML file that creates the entire user interface using Tailwind CSS. Its embedded JavaScript handles all user interactions, such as sending questions to the backend and rendering the streaming text or chart responses.

---

## 🚀 How to Run This Project

Follow these steps precisely to get the application running on your local machine.

### Step 1: Prerequisites

* Make sure you have **Python 3.8** or newer installed.
* You will need `pip` (Python's package installer), which typically comes with Python.

### Step 2: Backend Setup

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/ReddyAkash/AI-Agent-Anarix.git
    cd AI-Agent-Anarix
    ```

2.  **Navigate to the Backend Directory:**
    ```bash
    cd backend
    ```

3.  **Create and Activate a Virtual Environment** (Highly Recommended):
    * **Windows:**
        ```bash
        python -m venv .venv
        .\.venv\Scripts\activate
        ```
    * **macOS / Linux:**
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Set Up Your API Key:**
    * Create a file named `.env` inside the `backend` directory.
    * Add your Gemini API key to this file (get a key from [Google AI Studio](https://aistudio.google.com/)). The content should be:
        ```
        GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```

6.  **Add Your Data:**
    * Place your three CSV files (`ad_sales.csv`, `total_sales.csv`, `eligibility.csv`) inside the `backend/data/` directory.

### Step 3: Run the Application

1.  **Start the Server:**
    * While inside the `backend` directory, run the following command in your terminal:
        ```bash
        python run.py
        ```

2.  **Check the Terminal Output:**
    * You should see output confirming the database was created, followed by Uvicorn starting the server. The last line should look like this:
        ```
        INFO:     Uvicorn running on [http://0.0.0.0:8000](http://0.0.0.0:8000) (Press CTRL+C to quit)
        ```

### Step 4: Access the Frontend

1.  **Open Your Web Browser:**
    * Wait for 1 to 2 seconds the chatbot automatically opens in the browser or else navigate to the following URL: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
2.  The chat interface should load, and you can now start asking questions!

---

## 💬 Example Questions to Ask the Agent

* **Simple Data Query:** `what is my total sales?`
* **Conversational Query:** `hello, who are you?`
* **Data related Query:** `which product had the highest cpc?`