// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'

export default function App() {
  return (
    <div className="w-screen h-screen flex flex-col items-center justify-center bg-gradient-to-r from-indigo-500 to-pink-500">
      <h1 className="text-5xl font-bold text-white mb-6">🎸 Guitar Practice App</h1>
      <p className="text-lg text-white/90">
        If you can see this, Tailwind and React are alive and kicking.
      </p>
      <button className="mt-8 px-6 py-3 rounded-2xl bg-white text-indigo-600 font-semibold shadow-lg hover:scale-105 transition">
        Generate Song
      </button>
    </div>
  )
}
