import uvicorn
from app.database_setup import setup_database

if __name__ == "__main__":
    setup_database()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)