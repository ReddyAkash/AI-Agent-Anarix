from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from app.llm_helper import (
    get_sql_query,
    execute_sql_query,
    get_human_readable_answer_stream,
    get_general_response,
)
import os

# Initialize FastAPI
app = FastAPI(
    title="E-commerce AI Agent API",
    description="An API that answers questions about e-commerce data using an LLM.",
    version="1.1.0"
)

# Frontend directory
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend'))
app.mount("/static", StaticFiles(directory=frontend_dir, html=True), name="static")

# Serve index.html
@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class QuestionRequest(BaseModel):
    question: str

# Optional status check
@app.get("/status", summary="Status Check")
async def read_root():
    return {"message": "Welcome to the E-commerce AI Agent API!"}

# Main endpoint
@app.post("/ask", summary="Ask a Question")
async def ask_question(request: QuestionRequest):
    async def stream_generator():
        try:
            question_lower = request.question.lower()

            # Step 1: Handle known questions (CPC)
            if "cpc" in question_lower and any(word in question_lower for word in ["highest", "max", "top"]):
                print("CPC question detected. Using hardcoded SQL.")
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
                # Step 2: Ask LLM to generate SQL or say NO_SQL_NEEDED
                print("General question detected. Asking LLM for SQL query.")
                sql_query = get_sql_query(request.question).strip()

                # Step 3: If no SQL is needed, generate friendly reply
                if sql_query.upper() == "NO_SQL_NEEDED":
                    print("General conversation detected. Responding without SQL.")
                    for chunk in get_general_response(request.question):
                       yield chunk
                    return

            print(f"Executing SQL Query: {sql_query}")

            # Step 4: Execute SQL
            query_result = execute_sql_query(sql_query)
            if isinstance(query_result, str) and "Error:" in query_result:
                yield query_result
                return

            # Step 5: Stream human-readable reply
            for chunk in get_human_readable_answer_stream(request.question, query_result):
                yield chunk

        except Exception as e:
            print(f"Unexpected error in stream_generator: {e}")
            yield f"An unexpected error occurred: {str(e)}"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")


