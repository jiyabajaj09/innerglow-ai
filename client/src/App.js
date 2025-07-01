import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [page, setPage] = useState(1);
  const [thought, setThought] = useState('');
  const [reframed, setReframed] = useState('');

  useEffect(() => {
    const handleMouseMove = (e) => {
      document.documentElement.style.setProperty('--x', `${e.clientX}px`);
      document.documentElement.style.setProperty('--y', `${e.clientY}px`);
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const reframe = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/reframe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ thought }),
      });
      const data = await res.json();
      setReframed(data.reframed_thought);
    } catch (error) {
      setReframed("Oops! Something went wrong.");
    }
  };

  return (
    <>
      {page === 1 && (
        <div
          className="background"
          style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/bg.jpg)` }}
        >
          <div className="light-effect"></div>
          <div className="content">
            <h1>INNERGLOW</h1>
            <h2>You Are Your Own Therapist</h2>
            <button onClick={() => setPage(2)}>Let your inner light shine</button>
          </div>
        </div>
      )}

      {page === 2 && (
        <div className="page-two">
          <h2>Your Positive Voice</h2>
          <textarea
            value={thought}
            onChange={(e) => setThought(e.target.value)}
            placeholder="Talk to me…"
          />
          <button className="reframe-btn" onClick={reframe}>Reframe</button>
          {reframed && (
            <div className="reframed">{reframed}</div>
          )}
        </div>
      )}
    </>
  );
}

export default App;
