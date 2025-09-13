import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env file
load_dotenv()

MODEL = os.getenv("MODEL", "gpt-5-nano")

SYSTEM = """You generate simple beginner-friendly guitar chord arrangements intended for beginner level guitar practice and learning. 
Constraints:
- Use only basic open chords (e.g., C, G, D, E, A, Am, Em, Dm, E7, D7, A7, C7, Fmaj7, G7, Em7, Am7, Asus2, Asus4, Dsus2, Dsus4, D/F#).
- Use standard tuning (EADGBE).
- Output only valid JSON (no explanatory text) matching this schema:
{
  "title": "string, the name of the practice song",
  "key": "string, the key used (repeat the input key)",
  "bpm": 100,
  "time_signature": "4/4",
  "tuning": "Standard EADGBE",
  "capo": 0,
  "progression": ["C", "Am", "Fmaj7", "G", "C", "Am", "Fmaj7", "G"],
  "strum_pattern": "D D U U D U",
  "recommended_shapes": {
    "C": { "fingering": [-1, 3, 2, 0, 1, 0], "suggested": true, "label": null },
    "Am": { "fingering": [-1, 0, 2, 2, 1, 0], "suggested": true, "label": null },
    "Fmaj7": { "fingering": [-1, -1, 3, 2, 1, 0], "suggested": true, "label": null },
    "G": { "fingering": [3, 2, 0, 0, 0, 3], "suggested": true, "label": null }
  },
  "ascii_tabs": {
    "C": "e|-0-| B|-1-| G|-0-| D|-2-| A|-3-| E|---|",
    "Am": "e|-0-| B|-1-| G|-2-| D|-2-| A|-0-| E|---|",
    "Fmaj7": "e|-0-| B|-1-| G|-2-| D|-3-| A|---| E|---|",
    "G": "e|-3-| B|-0-| G|-0-| D|-0-| A|-2-| E|-3-|"
  }
}
"""

USER = """Make a practice progression in {key} with mood {mood}. 
It should be 16 bars, with a 4/4 time signature and a BPM between 90 and 120.
"""

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

def call_llm(key="C major", mood="happy"):
  resp = client.chat.completions.create(
    model=MODEL,
    messages=[
      {"role": "system", "content": SYSTEM},
      {"role": "user", "content": USER.format(key=key, mood=mood)}
    ],
    # temperature=0.6,
    response_format={"type": "json_object"}
  )
  return json.loads(resp.choices[0].message.content)