import './App.css';
import { useState } from 'react';
import type { Song } from './types';
import { ChordDiagram } from './components/diagram';

export default function App() {
  const [key, setKey] = useState('C major');
  const [mood, setMood] = useState('happy');
  const [song, setSong] = useState<Song | null>(null);
  const [genre, setGenre] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function generateSong() {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch('http://localhost:8000/generate_song', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key, mood, genre }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        setError(JSON.stringify(err, null, 2));
        return;
      }

      const data: Song = await res.json();
      setSong(data);
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen w-screen flex flex-col justify-center items-center bg-gradient-to-r from-indigo-500 to-pink-500/90 p-4">
      <div className="flex flex-col items-center gap-4 mx-16">
        <h1 className="text-2xl font-bold">GuitarBot - AI Guitar Song Generator</h1>

        {/* Form */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            generateSong();
          }}
          className="flex flex-col md:flex-row items-center gap-2 mx-4"
        >
          <input value={key} onChange={(e) => setKey(e.target.value)} className="p-2 border rounded" placeholder="Key (e.g., C major)" />
          <input value={mood} onChange={(e) => setMood(e.target.value)} className="p-2 border rounded" placeholder="Mood (e.g., happy)" />
          <input value={genre} onChange={(e) => setGenre(e.target.value)} className="p-2 border rounded" placeholder="Genre (optional)" />
          <button type="submit" className="px-4 py-2 bg-indigo-600 text-white rounded disabled:opacity-50" disabled={loading}>
            {loading ? 'Generating...' : song ? 'Try Another?' : 'Generate'}
          </button>
        </form>
      </div>

      {/* Error display */}
      {error && (
        <section className="mb-4">
          <h3 className="font-semibold text-red-500">Error</h3>
          <pre className="bg-black text-white p-3 rounded overflow-auto text-sm">{error}</pre>
        </section>
      )}

      {/* Song display */}
      {song && (
        <>
          <section className="mb-4">
            <h3 className="font-semibold">Summary</h3>
            <p>
              <strong>Title:</strong> {song.title || 'Untitled'}
            </p>
            <p>
              <strong>Key:</strong> {song.key} • <strong>BPM:</strong> {song.bpm}
            </p>
            <p>
              <strong>Strum:</strong> {song.strum_pattern.join(' ')}
            </p>

            <div className="mt-3">
              <h4 className="font-semibold">Progression (16 bars)</h4>
              <div className="flex flex-wrap gap-2 mt-2">
                {song.progression.map((c, i) => (
                  <div key={i} className="px-2 py-1 bg-indigo-100 text-indigo-900 rounded">
                    {c}
                  </div>
                ))}
              </div>
            </div>
          </section>

          <section className="mb-4">
            <h3 className="font-semibold">Chord Diagrams</h3>
            <div className="flex flex-wrap gap-6 justify-center mt-2">
              {song.progression.map((chordName: string, i: number) => {
                const shape = song.recommended_shapes[chordName];
                if (!shape) return null; // skip if no fingering available

                return (
                  <ChordDiagram
                    key={i} // use index to preserve order
                    chordName={chordName}
                    fingering={shape.fingering}
                  />
                );
              })}
            </div>
          </section>

          <section>
            <h3 className="font-semibold">Raw JSON</h3>
            <pre className="bg-gray-900 text-white p-3 rounded overflow-auto text-sm">{JSON.stringify(song, null, 2)}</pre>
          </section>
        </>
      )}
    </main>
  );
}

// export default App

// import React, { useState } from "react";

// type Song = any;

// export default function App() {
//   const [key, setKey] = useState("C major");
//   const [mood, setMood] = useState("happy");
//   const [song, setSong] = useState<Song | null>(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState<string | null>(null);

//   async function generateSong() {
//     setLoading(true);
//     setError(null);
//     setSong(null);
//     try {
//       const res = await fetch("http://localhost:8000/generate_song", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ key, mood }),
//       });

//       if (!res.ok) {
//         const err = await res.json().catch(() => ({ detail: res.statusText }));
//         setError(JSON.stringify(err, null, 2));
//       } else {
//         const data = await res.json();
//         setSong(data);
//       }
//     } catch (e) {
//       setError(String(e));
//     } finally {
//       setLoading(false);
//     }
//   }

//   return (
//     <main className="p-6 max-w-4xl mx-auto">
//       <h1 className="text-2xl font-bold mb-4">AI Guitar Song Generator — Test UI</h1>

//       <div className="flex gap-2 mb-4">
//         <input value={key} onChange={(e) => setKey(e.target.value)} className="input p-2 border rounded" />
//         <input value={mood} onChange={(e) => setMood(e.target.value)} className="input p-2 border rounded" />
//         <button className="btn px-4 py-2 bg-indigo-600 text-white rounded" onClick={generateSong} disabled={loading}>
//           {loading ? "Generating..." : "Generate"}
//         </button>
//       </div>

//       {error && (
//         <section className="mb-4">
//           <h3 className="font-semibold text-red-400">Error</h3>
//           <pre className="bg-black text-white p-3 rounded overflow-auto">{error}</pre>
//         </section>
//       )}

//       {song && (
//         <>
//           <section className="mb-4">
//             <h3 className="font-semibold">Summary</h3>
//             <p><strong>Title:</strong> {song.title}</p>
//             <p><strong>Key:</strong> {song.key} • <strong>BPM:</strong> {song.bpm} • <strong>Strum:</strong> {song.strum_pattern}</p>

//             <div className="mt-3">
//               <h4 className="font-semibold">Progression (16 bars)</h4>
//               <div className="flex flex-wrap gap-2 mt-2">
//                 {song.progression.map((c: string, i: number) => (
//                   <div key={i} className="px-2 py-1 bg-indigo-100 text-indigo-900 rounded">{c}</div>
//                 ))}
//               </div>
//             </div>
//           </section>

//           <section>
//             <h3 className="font-semibold">Raw JSON</h3>
//             <pre className="bg-gray-900 text-white p-3 rounded overflow-auto">{JSON.stringify(song, null, 2)}</pre>
//           </section>
//         </>
//       )}
//     </main>
//   );
// }
