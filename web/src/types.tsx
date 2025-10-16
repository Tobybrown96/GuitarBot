// TypeScript interfaces corresponding to Python data structures in schemas.py
// This file is referenced in web/src/App.tsx

export interface TabShape {
  fingering: number[];         // Python: List[int]
  suggested: boolean;          // Python: bool
  label?: string | null;       // Python: Optional[str]
}

export interface Song {
  title?: string | null;       // Python: Optional[str]
  key: string;                 // Python: str
  bpm: number;                 // Python: int
  time_signature: string;      // Python: str
  tuning: string;              // Python: str
  capo?: number | null;        // Python: Optional[int]
  progression: string[];       // Python: List[str]
  strum_pattern: string[];     // Python: List[str]
  recommended_shapes: Record<string, TabShape>; // Python: Dict[str, TabShape]
  ascii_tabs: Record<string, string>;           // Python: Dict[str, str]
}