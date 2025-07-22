from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import StreamingResponse
from app.llm_helper import get_sql_query, execute_sql_query, get_human_readable_answer_stream

app = FastAPI()

# CORS middleware to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(request: QuestionRequest):
    async def stream_answer():
        try:
            sql_query = get_sql_query(request.question)
            if not sql_query:
                yield "Could not generate SQL query."
                return

            query_result = execute_sql_query(sql_query)
            
            for chunk in get_human_readable_answer_stream(request.question, query_result):
                yield chunk

        except Exception as e:
            yield f"An error occurred: {str(e)}"

    return StreamingResponse(stream_answer(), media_type="text/event-stream")