import React, { useState } from "react";

export default function App() {
  const [page, setPage] = useState(1);
  const [thought, setThought] = useState("");
  const [reframed, setReframed] = useState("");

  async function reframe() {
    const response = await fetch("http://127.0.0.1:8000/reframe", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ thought }),
    });
    const data = await response.json();
    setReframed(data.reframed_thought);
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-pink-200 via-blue-200 to-purple-200 p-6 relative overflow-hidden text-center font-sans">
      {/* animated glowing circles */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-pink-200 opacity-30 rounded-full blur-3xl animate-pulse"></div>
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-blue-200 opacity-30 rounded-full blur-3xl animate-pulse"></div>

      {page === 1 && (
        <div className="z-10 flex flex-col items-center justify-center space-y-8 animate-fade-in">
          <h1 className="text-7xl font-extrabold text-pink-500 drop-shadow-[0_0_15px_rgba(236,72,153,0.6)]">
            INNERGLOW
          </h1>
          <h2 className="text-3xl text-blue-500 font-semibold drop-shadow-[0_0_8px_rgba(59,130,246,0.5)]">
            You Are Your Own Therapist
          </h2>
          <button
            onClick={() => setPage(2)}
            className="mt-6 px-10 py-4 text-2xl font-bold text-white bg-purple-500 rounded-full shadow-xl hover:scale-105 hover:bg-purple-600 transition transform duration-200 ease-out"
          >
            Let your inner light shine
          </button>
        </div>
      )}

      {page === 2 && (
        <div className="z-10 flex flex-col items-center w-full max-w-2xl space-y-8 animate-fade-in">
          <h2 className="text-5xl font-bold text-pink-500 drop-shadow-[0_0_10px_rgba(236,72,153,0.5)]">
            Your Positive Voice
          </h2>
          <textarea
            value={thought}
            onChange={(e) => setThought(e.target.value)}
            placeholder="Talk to me…"
            className="w-full p-6 h-48 text-xl text-center bg-white/80 border-4 border-blue-200 rounded-xl focus:border-blue-400 focus:outline-none shadow-xl resize-none"
          ></textarea>
          <button
            onClick={reframe}
            className="px-8 py-3 text-xl font-bold text-white bg-pink-400 rounded-full shadow-xl hover:bg-pink-500 transition transform hover:scale-105"
          >
            Reframe
          </button>
          {reframed && (
            <p className="mt-8 p-6 w-full text-center text-2xl font-medium bg-white/80 border-2 border-purple-200 rounded-xl text-purple-700 shadow-2xl animate-fade-in">
              {reframed}
            </p>
          )}
        </div>
      )}

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;800&display=swap');

        @keyframes fade-in {
          from { opacity: 0; transform: scale(0.9); }
          to { opacity: 1; transform: scale(1); }
        }
        .animate-fade-in {
          animation: fade-in 0.8s ease-in-out;
        }
      `}</style>
    </div>
  );
}
