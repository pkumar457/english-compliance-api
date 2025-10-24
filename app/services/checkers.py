
from typing import List, Dict, Any, Tuple
import spacy, textstat
from language_tool_python import LanguageTool
from app.models.schemas import RuleIssue, ComplianceReport

try:
    _NLP = spacy.load("en_core_web_sm")
except Exception:
    _NLP = spacy.blank("en")
try:
    _LT = LanguageTool('en-US'); _LT_AVAILABLE = True
except Exception:
    _LT_AVAILABLE = False

def _grammar_issues(text: str) -> List[RuleIssue]:
    out=[]; 
    if not _LT_AVAILABLE: return out
    for m in _LT.check(text[:100000]):
        out.append(RuleIssue(rule_id=f"grammar/{m.ruleId}", severity="error" if m.ruleIssueType in ("misspelling","typographical") else "warn", message=m.message, start_char=m.offset, end_char=m.offset+m.errorLength, sentence=m.context, suggestions=[r.value for r in m.replacements][:3]))
    return out

def _sentence_stats_and_length_issues(text: str)->Tuple[Dict[str,Any],List[RuleIssue]]:
    if not text.strip(): return {}, []
    doc=_NLP(text); has_sents=doc.has_annotation("SENT_START")
    lens=[len([t for t in s if not t.is_space]) for s in doc.sents] if has_sents else []
    issues=[]
    if has_sents:
        for s,l in zip(doc.sents,lens):
            if l>30: issues.append(RuleIssue(rule_id="sent_length/too_long",severity="error",message=f"Very long sentence ({l} words). Consider splitting.",start_char=s.start_char,end_char=s.end_char,sentence=s.text))
            elif l>25: issues.append(RuleIssue(rule_id="sent_length/long",severity="warn",message=f"Long sentence ({l} words).",start_char=s.start_char,end_char=s.end_char,sentence=s.text))
    avg=sum(lens)/len(lens) if lens else 0
    return {"sentences":len(lens),"avg_sentence_length":round(avg,2)}, issues

def _passive_voice_issues(text:str)->List[RuleIssue]:
    if "tagger" not in _NLP.pipe_names or "parser" not in _NLP.pipe_names: return []
    doc=_NLP(text); issues=[]
    for s in doc.sents:
        if any(t.dep_=="auxpass" for t in s) and any(t.tag_=="VBN" for t in s):
            issues.append(RuleIssue(rule_id="passive/auxpass",severity="warn",message="Possible passive voice; consider rewriting in active voice.",start_char=s.start_char,end_char=s.end_char,sentence=s.text))
    return issues

def _readability_metrics(text:str)->Dict[str,Any]:
    if not text.strip(): return {}
    return {
        "flesch_reading_ease": textstat.flesch_reading_ease(text),
        "flesch_kincaid_grade": textstat.flesch_kincaid_grade(text),
        "gunning_fog": textstat.gunning_fog(text),
        "text_standard": textstat.text_standard(text, float_output=False),
    }

def check_compliance(text:str)->ComplianceReport:
    issues=[]; issues+=_grammar_issues(text)
    stats, len_issues=_sentence_stats_and_length_issues(text); issues+=len_issues
    issues+=_passive_voice_issues(text)
    metrics={}; metrics.update(stats); metrics.update(_readability_metrics(text))
    ok=all(i.severity!="error" for i in issues)
    return ComplianceReport(ok=ok,guideline_summary={"Grammar":"See LanguageTool checks","Sentence length":"<=25 words preferred; >30 flagged","Passive voice":"Prefer active voice","Readability":"Target grades 8–10"},issues=issues,metrics=metrics)
