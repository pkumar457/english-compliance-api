
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class RuleIssue(BaseModel):
    rule_id: str
    severity: str = Field(description="one of: info, warn, error")
    message: str
    start_char: int | None = None
    end_char: int | None = None
    sentence: str | None = None
    suggestions: List[str] = []

class ComplianceReport(BaseModel):
    ok: bool
    guideline_summary: Dict[str, Any]
    issues: List[RuleIssue] = []
    metrics: Dict[str, Any] = {}

class AnalyzeResponse(BaseModel):
    report: ComplianceReport
    extracted_text_preview: str
    document_id: str

class RewriteRequest(BaseModel):
    document_id: str
    strategy: str = Field(default="auto", description="auto | grammar_only | style | gpt")
    tone: Optional[str] = Field(default=None, description="e.g., formal, neutral, friendly")
    target_readability: Optional[str] = Field(default="8-10", description="target grade range for textstat")

class RewriteResponse(BaseModel):
    document_id: str
    original_char_count: int
    revised_char_count: int
    download_filename: str
