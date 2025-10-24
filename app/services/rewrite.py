
from typing import List
import os, re
from docx import Document as DocxDocument
from language_tool_python import LanguageTool

try:
    import spacy
    _NLP = spacy.load("en_core_web_sm")
except Exception:
    _NLP = spacy.blank("en")
try:
    from openai import OpenAI
    _OPENAI = OpenAI(); _HAS_OPENAI=True
except Exception:
    _HAS_OPENAI=False

def _lt_fix(text:str)->str:
    try: lt=LanguageTool('en-US')
    except Exception: return text
    fixed=text
    for m in sorted(lt.check(text[:100000]), key=lambda x:x.offset, reverse=True):
        repl=m.replacements[0].value if m.replacements else None
        if repl and m.errorLength>0: fixed=fixed[:m.offset]+repl+fixed[m.offset+m.errorLength:]
    return fixed

def _style_cleanup(text:str, target_readability:str|None="8-10")->str:
    if "sentencizer" not in _NLP.pipe_names: _NLP.add_pipe("sentencizer")
    out=[]
    for s in _NLP(text).sents:
        sent=s.text.strip()
        sent=re.sub(r"\b(is|was|were|be|been|being|are|am) ([a-zA-Z]+ed)\b", r"\2", sent)
        sent=re.sub(r"\b(really|very|basically|actually|just|quite|kind of|sort of)\b","",sent,flags=re.I)
        sent=re.sub(r"\s{2,}"," ",sent).strip()
        words=sent.split()
        if len(words)>30:
            mid=len(words)//2
            out.append(" ".join(words[:mid])+".")
            out.append(" ".join(words[mid:]).capitalize())
        else:
            out.append(sent)
    return " ".join(out)

def _gpt_rewrite(text:str,tone:str|None,tr:str|None)->str:
    if not _HAS_OPENAI: return text
    from openai import OpenAI
    sys="You are an expert English editor. Rewrite to comply with standard English writing guidelines: correct grammar and punctuation, prefer active voice, keep sentences <= 25 words when possible, be concise and clear, and target a reading level of grades 8–10. Preserve meaning and facts. Return only the revised text."
    if tone: sys+=f" Use a {tone} tone."
    try:
        resp=_OPENAI.chat.completions.create(model=os.environ.get("OPENAI_MODEL","gpt-4o-mini"),temperature=0.2,messages=[{"role":"system","content":sys},{"role":"user","content":text}])
        return resp.choices[0].message.content.strip()
    except Exception:
        return text

def rewrite_text(text:str,strategy:str="auto",tone:str|None=None,target_readability:str|None="8-10")->str:
    if strategy=="grammar_only": return _lt_fix(text)
    if strategy=="style": return _style_cleanup(_lt_fix(text),target_readability)
    if strategy=="gpt": return _gpt_rewrite(text,tone,target_readability)
    revised=_style_cleanup(_lt_fix(text),target_readability)
    if os.environ.get("OPENAI_API_KEY"): revised=_gpt_rewrite(revised,tone,target_readability)
    return revised

def write_docx(text:str,path:str)->None:
    doc=DocxDocument()
    for para in text.split("\n"): doc.add_paragraph(para)
    doc.save(path)
