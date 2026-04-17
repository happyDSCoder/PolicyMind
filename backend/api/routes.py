from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.models.schemas import QuestionRequest, AnswerResponse
from backend.core.rag import ask_question
from backend.graph.ingestor import ingest_document
import tempfile, os

router = APIRouter()


@router.post("/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):
    try:
        result = ask_question(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        ingest_document(tmp_path, source_name=file.filename)
        return {"message": f"{file.filename} ingested successfully."}
    finally:
        os.unlink(tmp_path)