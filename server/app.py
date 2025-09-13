from fastapi import FastAPI, HTTPException
from schemas import Song
from services.llm import call_llm

app = FastAPI(title="Guitar Practice API")

@app.get("/health")
def health():
    return {"healthy": True}

@app.post("/generate_song", response_model=Song)
def generate_song(key: str = "C", mood: str = "happy"):
  try:
    raw=call_llm(key, mood)
    return Song(**raw) # Validation
  except Exception as e:
    raise HTTPException(status_code=502, detail=str(e))


