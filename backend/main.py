from fastapi import FastAPI, UploadFile,File
from fastapi.middleware.cors import CORSMiddleware

import os

from app import process_document,ask_question



app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = f"uploaded_{file.filename}"

    # Read PDF only once
    content = await file.read()

    # Save PDF
    with open(file_path, "wb") as f:
        f.write(content)

    # Process the same PDF bytes
    chunks = process_document(file_path)

    return {
        "message": "pdf processed successfully",
        "chunks": chunks
    }

@app.post("/ask")
async def ask(query:dict):

    question=query.get("question")

    if not question:
        return{
            "error": "question is requered"
        }
    answer=ask_question(question)

    return {
        "question":question,
        "answer": answer
    }


@app.get("/")
def home():

    return{
        "message": "rag api is running"
        
    }
