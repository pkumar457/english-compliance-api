
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers.analyze import router as analyze_router

app = FastAPI(title="English Compliance API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(analyze_router)

@app.get("/healthz")
async def healthz():
    return JSONResponse({"ok": True})
