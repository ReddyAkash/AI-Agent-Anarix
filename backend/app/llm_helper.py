import os
import google.generativeai as genai
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

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
You are an expert SQL assistant. Based on the database schema below, generate a precise SQL query to answer the user's question.

⚠️ VERY IMPORTANT RULES:
1. CPC = ad_spend / clicks
2. RoAS = ad_sales / ad_spend
3. Avoid division by zero (use WHERE clicks > 0 or ad_spend > 0)
4. Return SQL only, without any markdown or commentary.

📘 EXAMPLES:

Q: Which product has the highest CPC?
SQL: SELECT item_id, ad_spend * 1.0 / clicks AS cpc FROM ad_sales WHERE clicks > 0 ORDER BY cpc DESC LIMIT 1;

Q: What is the total number of units sold?
SQL: SELECT SUM(units_sold) AS total_units_sold FROM ad_sales;

    Schema:
    {schema}

    Question: {question}
    SQL Query:
    """
    response = model.generate_content(prompt)
    print("Prompt sent to Gemini:\n", prompt)
    print("Raw LLM response:\n", response.text)
    response_text = response.text.strip().replace('`', '').replace('sql', '').strip()
    sql_query = response_text.split(';')[0].strip() + ';'
    return sql_query

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