// import { useEffect, useRef } from "react";
import Chord from "@techies23/react-chords";

interface ChordDiagramProps {
  chordName: string;
  fingering: number[]; // backend: [-1, 3, 2, 0, 1, 0]
}

const instrument = {
  strings: 6,
  fretsOnChord: 4,
  name: "Guitar",
  keys: [],
  tunings: {
    standard: ["E", "A", "D", "G", "B", "E"],
  },
};

export function ChordDiagram({ chordName, fingering }: ChordDiagramProps) {
  // Convert backend fingering array into library format
  const frets = fingering.map((f) => (f < 0 ? 0 : f)); // -1 muted → 0
  const fingers = frets.map((f) => (f > 0 ? 1 : 0));   // placeholder
  const barres: number[] = [];

  const chord = {
    frets,
    fingers,
    barres,
    capo: false,
  };

  return (
    <div className="p-2 flex flex-col items-center">
      <span className="mb-1 font-medium">{chordName}</span>
      <Chord chord={chord} instrument={instrument} lite={false} />
    </div>
  );
}