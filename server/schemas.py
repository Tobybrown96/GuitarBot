from pydantic import BaseModel
from typing import Dict, List

class TabShape(BaseModel):
  fingering: List[int] # [-1,3,2,0,1,0] style
  suggested: bool = True
  label: str | None = None

class Song(BaseModel):
  title: str
  key: str
  bpm: int
  time_signature: str
  tuning: str
  capo: int
  progression: List[str]
  strum_pattern: str
  recommended_shapes: Dict[str, TabShape]
  ascii_tabs: Dict[str,str]
