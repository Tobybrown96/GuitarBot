from typing import Dict, List, Any
import re

ALLOWED_CHORDS = {
   "C", "G", "D", "E", "A", "Am", "Em", "Dm", "Cadd9", "E7", "D7", "A7", "C7", "Fmaj7", "G7", "Em7", "Am7", "Asus2", "Asus4", "Dsus2", "Dsus4", "D/F#"
}

def validate_song_data(data: Dict[str, Any]) -> None:
  errors = []

  # top-level type check
  if not isinstance(data, dict):
    raise ValueError("Model did not return a JSON object.")
  
  # progression 
  prog = data.get("progression")
  if not isinstance(prog, list) or not all(isinstance(chord, str) for chord in prog):
    errors.append("Field 'progression' must be a list of strings.")
  else:
    if len(prog) != 16:
      errors.append("Field 'progression' must contain exactly 16 chords.")
    if any(chord not in ALLOWED_CHORDS for chord in prog):
      invalid_chords = [chord for chord in prog if chord not in ALLOWED_CHORDS]
      errors.append(f"Field 'progression' contains invalid chords: {invalid_chords}. Allowed chords are: {sorted(ALLOWED_CHORDS)}.")
  
  # recommended_shapes
  rec = data.get("recommended_shapes")
  if not isinstance(rec, dict):
    errors.append("Field 'recommended_shapes' must be a dictionary.")
  else:
    if isinstance(prog, list):
      for chord in set(prog):
        if chord not in rec:
          errors.append(f"Field 'recommended_shapes' is missing an entry for chord '{chord}' used in 'progression'.")

    for chord, shape in rec.items():
      if chord not in ALLOWED_CHORDS:
        errors.append(f"Field 'recommended_shapes' contains invalid chord '{chord}'. Allowed chords are: {sorted(ALLOWED_CHORDS)}.")
      if not isinstance(shape, dict):
        errors.append(f"Shape for chord '{chord}' must be a dictionary.")
        continue
      
      fingering = shape.get("fingering")
      if not isinstance(fingering, list) or len(fingering) != 6 or not all(isinstance(f, int) for f in fingering):
        errors.append(f"Fingering for chord '{chord}' must be a list of 6 integers.")
      # suggested = shape.get("suggested")
      # if not isinstance(suggested, bool):
      #   errors.append(f"'suggested' for chord '{chord}' must be a boolean.")
      # label = shape.get("label")
      # if label is not None and not isinstance(label, str):
      #   errors.append(f"'label' for chord '{chord}' must be a string or null.")

  # ascii_tabs
  tabs = data.get("ascii_tabs")
  if not isinstance(tabs, dict):
    errors.append("Field 'ascii_tabs' must be a dictionary.")
  else:
    if isinstance(prog, list):
      for chord in set(prog):
        if chord not in tabs:
          errors.append(f"Field 'ascii_tabs' is missing an entry for chord '{chord}' used in 'progression'.")

    tab_pattern = re.compile(r"^(e|B|G|D|A|E)\|([-0-9x|]+)\|$")
    for chord, tab in tabs.items():
      if chord not in ALLOWED_CHORDS:
        errors.append(f"Field 'ascii_tabs' contains invalid chord '{chord}'. Allowed chords are: {sorted(ALLOWED_CHORDS)}.")
      if not isinstance(tab, str):
        errors.append(f"Tab for chord '{chord}' must be a string.")
        continue
      
      lines = tab.strip().split("\n")
      if len(lines) != 6:
        errors.append(f"Tab for chord '{chord}' must have exactly 6 lines (one per string).")
        continue
      
      strings_seen = set()
      for line in lines:
        match = tab_pattern.match(line.strip())
        if not match:
          errors.append(f"Line '{line}' in tab for chord '{chord}' is not properly formatted.")
          continue
        string_name = match.group(1)
        if string_name in strings_seen:
          errors.append(f"Duplicate string '{string_name}' in tab for chord '{chord}'.")
        strings_seen.add(string_name)
      
      if strings_seen != {"e", "B", "G", "D", "A", "E"}:
        errors.append(f"Tab for chord '{chord}' must include all six strings: e, B, G, D, A, E.")

  # bpm
  bpm = data.get("bpm")
  if not isinstance(bpm, int) or not (40 <= bpm <= 240):
    errors.append("Field 'bpm' must be an integer between 40 and 240.")

  # strum_pattern
  strum = data.get("strum_pattern")
  if not isinstance(strum, list) or len(strum) != 6 or not all(s in {"D", "U"} for s in strum):
    errors.append("Field 'strum_pattern' must be a list of 6 strings, each either 'D' or 'U'.")

  if errors:
    raise ValueError("Validation errors:\n" + "\n".join(errors))