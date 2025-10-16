from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from schemas import Song
from services.llm import call_llm
from utils.validation import validate_song_data

app = FastAPI(title="Guitar Practice API")

# allow React dev server
origins = [
  "http://localhost:5173",
  "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    key: str
    mood: str
    genre: str | None = None

@app.get("/health")
def health():
    return {"healthy": True}

@app.post("/generate_song", response_model=Song)
def generate_song(request: GenerateRequest):
  try:
    raw = call_llm(request.key, request.mood, request.genre)
    # validate_song_data(raw) # custom validation
    return Song(**raw)
  except Exception as e:
    raise HTTPException(status_code=502, detail=str(e))

    # 2) Validate structure and types
  try:
    validate_song_data(raw)
    validated = Song(**raw) # Pydantic validation
    return validated
  except Exception as ve:
    raise HTTPException(
      status_code=502,
      detail={
      "error": "model_validation_failed",
      "first_error": str(ve)
      }
    )