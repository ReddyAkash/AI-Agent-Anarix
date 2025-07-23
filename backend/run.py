import uvicorn
import threading
import webbrowser
from app.database_setup import setup_database

def open_browser():
    webbrowser.open_new("http://localhost:8000/")

if __name__ == "__main__":
    setup_database()
    threading.Timer(1.5, open_browser).start()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
