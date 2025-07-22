from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from app.llm_helper import get_sql_query, execute_sql_query, get_human_readable_answer_stream

# Initialize the FastAPI app
app = FastAPI(
    title="E-commerce AI Agent API",
    description="An API that answers questions about e-commerce data using an LLM.",
    version="1.1.0"
)

# Configure CORS (Cross-Origin Resource Sharing) middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model for the /ask endpoint
class QuestionRequest(BaseModel):
    question: str

@app.get("/", summary="Root Endpoint", description="A simple root endpoint to check if the server is running.")
async def read_root():
    return {"message": "Welcome to the E-commerce AI Agent API!"}


@app.post("/ask", summary="Ask a Question", description="Receives a question, gets an answer from the LLM, and streams it back.")
async def ask_question(request: QuestionRequest):
    """
    This is the main endpoint. It uses a hybrid approach:
    1. It checks for specific, known-problematic questions (like "highest CPC").
    2. If a known question is detected, it uses a hardcoded, guaranteed-correct SQL query.
    3. For all other questions, it falls back to using the LLM to generate the SQL query.
    """
    async def stream_generator():
        try:
            sql_query = ""
            question_lower = request.question.lower()

            # --- HYBRID LOGIC ---
            # Check if the user is asking for the highest or maximum CPC.
            if "cpc" in question_lower and ("highest" in question_lower or "max" in question_lower or "top" in question_lower):
                print("CPC question detected. Using hardcoded, reliable SQL query.")
                # This query is guaranteed to be correct.
                sql_query = """
                    SELECT
                      item_id,
                      CAST(ad_spend AS REAL) / clicks AS cpc
                    FROM
                      ad_sales
                    WHERE
                      clicks > 0
                    ORDER BY
                      cpc DESC
                    LIMIT 1;
                """
            else:
                # Fallback to the LLM for all other general questions.
                print("General question detected. Asking LLM for SQL query.")
                sql_query = get_sql_query(request.question)
            # --- END OF HYBRID LOGIC ---

            # We still log the query being executed for debugging purposes.
            print(f"Executing SQL Query: {sql_query}")

            if not sql_query or "Error:" in sql_query:
                yield "Could not generate or determine a valid SQL query."
                return

            # Step 2: Execute the SQL query
            query_result = execute_sql_query(sql_query)
            if isinstance(query_result, str) and "Error:" in query_result:
                 yield query_result
                 return

            # Step 3: Stream the final human-readable answer from the LLM.
            for chunk in get_human_readable_answer_stream(request.question, query_result):
                yield chunk

        except Exception as e:
            print(f"An unexpected error occurred in stream_generator: {e}")
            yield f"An unexpected error occurred: {str(e)}"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")