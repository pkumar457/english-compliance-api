
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import os, uuid
from typing import Dict
from app.services.extract import extract_text
from app.services.checkers import check_compliance
from app.services.rewrite import rewrite_text, write_docx
from app.models.schemas import AnalyzeResponse, RewriteRequest, RewriteResponse

STORE_DIR = os.environ.get("STORE_DIR", "/tmp/eca_store")
os.makedirs(STORE_DIR, exist_ok=True)
_DOCS: Dict[str, str] = {}

router = APIRouter(prefix="/v1", tags=["analysis"])

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_document(file: UploadFile = File(...)):
    filename = file.filename or "upload"
    if not (filename.lower().endswith(".pdf") or filename.lower().endswith(".docx")):
        raise HTTPException(status_code=400, detail="Only .pdf or .docx accepted")
    b = await file.read()
    try:
        mime_hint, text = extract_text(filename, b)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Text extraction failed: {e}")
    if not text or len(text.strip()) < 10:
        raise HTTPException(status_code=400, detail="No readable text found in the document")
    report = check_compliance(text)
    doc_id = str(uuid.uuid4())
    _DOCS[doc_id] = text
    return AnalyzeResponse(report=report, extracted_text_preview=text[:1000], document_id=doc_id)

@router.post("/rewrite", response_model=RewriteResponse)
async def rewrite_document(req: RewriteRequest):
    if req.document_id not in _DOCS:
        raise HTTPException(status_code=404, detail="document_id not found. Upload & analyze first.")
    original = _DOCS[req.document_id]
    revised = rewrite_text(original, strategy=req.strategy, tone=req.tone, target_readability=req.target_readability)
    out_name = f"revised_{req.document_id}.docx"
    write_docx(revised, os.path.join(STORE_DIR, out_name))
    return RewriteResponse(document_id=req.document_id, original_char_count=len(original), revised_char_count=len(revised), download_filename=out_name)

@router.get("/download/{filename}")
async def download(filename: str):
    safe = os.path.basename(filename)
    path = os.path.join(STORE_DIR, safe)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=safe)
