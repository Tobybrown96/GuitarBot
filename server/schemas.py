from pydantic import BaseModel
from typing import Dict, List, Optional

class TabShape(BaseModel):
  fingering: List[int] # [-1,3,2,0,1,0] style
  suggested: bool = True
  label: str | None = None

class Song(BaseModel):
  title: Optional[str] = None
  key: str
  genre: Optional[str] = None
  bpm: int
  time_signature: str
  tuning: str
  capo: Optional[int] = None
  progression: List[str]
  strum_pattern: List[str]
  recommended_shapes: Dict[str, TabShape]
  ascii_tabs: Dict[str,str]
