import json
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load variables from .env file
load_dotenv()

MODEL = os.getenv("MODEL", "gpt-5-nano")

SYSTEM = """You generate simple beginner-friendly guitar chord arrangements intended for beginner level guitar practice and learning. While following the constraints and complying with the schema below. Using music theory, you must make a musically interesting and enjoyable progression that best fits the users requested key, mood and/or genre.
Constraints:
- Use only basic open chords (e.g., C, G, D, E, A, Am, Em, Dm, Cadd9, E7, D7, A7, C7, Fmaj7, Cmaj7, Gmaj7, Bm, G7, Em7, Am7, B7, Asus2, Asus4, Dsus2, Dsus4, D/F#).
- If the user provides a genre, ensure the progression, strum pattern, tempo, etc., fit that genre. If no genre is provided, and then choose one that fits the mood and key.
- If the user provides a key that is not in the allowed chords, choose the closest sounding key that best fits the other user requests.
- No barre chords or complex jazz chords.
- Progression should contain no less than 5 unique chords.
- Progression should contain no more than 8 unique chords.
- Use standard tuning (EADGBE).
- Strum pattern should return a list of 6 strings, each either "D" or "U".
- Output only valid JSON (no explanatory text) matching this schema:
{
  "title": "string, the name of the practice song",
  "key": "string, the key used (repeat the input key)",
  "genre": "string, the genre used (repeat the input genre, or, if no genre was provided, fill in with a genre of your choosing that best fits the mood and key.)",
  "bpm": 100,
  "time_signature": "4/4",
  "tuning": "Standard EADGBE",
  "capo": 0,
  "progression": ["C", "Am", "Fmaj7", "G", "C", "Am", "Fmaj7", "G"],
  "strum_pattern": ["D", "D", "U", "U", "D", "U"],
  "recommended_shapes": {
    "C": { "fingering": [-1, 3, 2, 0, 1, 0] },
    "Am": { "fingering": [-1, 0, 2, 2, 1, 0] },
    "Fmaj7": { "fingering": [-1, -1, 3, 2, 1, 0] },
    "G": { "fingering": [3, 2, 0, 0, 0, 3] }
  },
  "ascii_tabs": {
    "C": "e|-0-| B|-1-| G|-0-| D|-2-| A|-3-| E|---|",
    "Am": "e|-0-| B|-1-| G|-2-| D|-2-| A|-0-| E|---|",
    "Fmaj7": "e|-0-| B|-1-| G|-2-| D|-3-| A|---| E|---|",
    "G": "e|-3-| B|-0-| G|-0-| D|-0-| A|-2-| E|-3-|"
  }
}
"""

  # "C": { "fingering": [-1, 3, 2, 0, 1, 0], "suggested": true, "label": null },
  # "Am": { "fingering": [-1, 0, 2, 2, 1, 0], "suggested": true, "label": null },
  # "Fmaj7": { "fingering": [-1, -1, 3, 2, 1, 0], "suggested": true, "label": null },
  # "G": { "fingering": [3, 2, 0, 0, 0, 3], "suggested": true, "label": null }

USER = """Make a beginner-friendly guitar chord progression in {key} with a {mood} mood. 
It should be 16 bars, with a 4/4 time signature and a BPM between 90 and 120.
Strum pattern should be some combination of D and U (down and up).
"""

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPEN_API_KEY"))

def call_llm(key="C major", mood="happy", genre=None):
  user_prompt = USER.format(key=key, mood=mood)
  if genre:
    user_prompt += f"The style should resemble {genre} music."

  resp = client.chat.completions.create(
    model=MODEL,
    messages=[
      {"role": "system", "content": SYSTEM},
      {"role": "user", "content": USER.format(key=key, mood=mood, genre=genre)}
    ],
    # temperature=0.6,
    response_format={"type": "json_object"}
  )
  return json.loads(resp.choices[0].message.content)