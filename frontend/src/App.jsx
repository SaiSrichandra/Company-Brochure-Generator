import { useState } from 'react';
import BrochureForm from './components/BrochureForm';
import AuthForm from './components/AuthForm';
import Dashboard from './components/Dashboard';

function App() {
  const [user, setUser] = useState(localStorage.getItem('username'));
  const [view, setView] = useState('generate');

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setUser(null);
    setView('generate');
  };

  if (!user) {
    return (
      <div className="App">
        <h1>AI Brochure Generator</h1>
        <AuthForm onAuth={(u) => setUser(u)} />
      </div>
    );
  }

  return (
    <div className="App">
      <div className="top-bar">
        <h1>AI Brochure Generator</h1>
        <div className="top-bar-right">
          <span style={{ color: '#00f2ff' }}>Hi, {user}</span>
          <button className="btn-secondary" onClick={() => setView(view === 'generate' ? 'dashboard' : 'generate')}>
            {view === 'generate' ? 'My Brochures' : 'Generate'}
          </button>
          <button className="btn-secondary" onClick={handleLogout}>Logout</button>
        </div>
      </div>
      {view === 'generate' ? <BrochureForm /> : <Dashboard onBack={() => setView('generate')} />}
    </div>
  );
}

export default App;
