import os
import google.generativeai as genai
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

db_path = os.path.join(os.path.dirname(__file__), 'ecommerce_data.db')
engine = create_engine(f'sqlite:///{db_path}')

def get_db_schema():
    """Gets the schema of the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result]
        schema = ""
        for table in tables:
            schema += f"Table '{table}':\n"
            result = connection.execute(text(f"PRAGMA table_info({table});"))
            columns = [f"  {row[1]} ({row[2]})" for row in result]
            schema += "\n".join(columns) + "\n\n"
    return schema

def get_sql_query(question: str) -> str:
    """Gets the SQL query from the LLM."""
    schema = get_db_schema()
    prompt = f"""
    Based on the database schema below, write a single, executable SQL query to answer the user's question.
Pay close attention to derived metrics like CPC (Cost Per Click) or RoAS (Return on Ad Spend).

**IMPORTANT RULES:**
1.  **CPC Calculation:** To calculate Cost Per Click, use the formula `ad_spend / clicks`.
2.  **Avoid Division by Zero:** When calculating CPC, you MUST exclude any rows where `clicks` is 0. Use a `WHERE clicks > 0` clause.
3.  Only return the SQL query and nothing else. Do not wrap it in markdown.

    Schema:
    {schema}

    Question: {question}
    SQL Query:
    """
    response = model.generate_content(prompt)
    return response.text.strip().replace('`', '').replace('sql', '').strip()

def execute_sql_query(query: str):
    """Executes the SQL query and returns the result."""
    with engine.connect() as connection:
        result = connection.execute(text(query))
        rows = result.fetchall()
        columns = result.keys()
        return [dict(zip(columns, row)) for row in rows]

def get_human_readable_answer_stream(question: str, query_result):
    """Gets a human-readable answer from the LLM as a stream."""
    prompt = f"""
    The user asked: '{question}'.
    The database result is: {query_result}.
    Provide a concise, human-readable answer. If the result is empty, say you couldn't find any data.
    """
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        yield chunk.text