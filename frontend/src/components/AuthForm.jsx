import { useState } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_URL;

function AuthForm({ onAuth }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    const endpoint = isLogin ? '/auth/login' : '/auth/register';

    try {
      const body = isLogin
        ? new URLSearchParams({ username, password })
        : JSON.stringify({ username, password });

      const headers = isLogin
        ? { 'Content-Type': 'application/x-www-form-urlencoded' }
        : { 'Content-Type': 'application/json' };

      const res = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers,
        body,
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Authentication failed');
      }

      const data = await res.json();
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('username', username);
      onAuth(username);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container">
      <h2 style={{ color: '#fff', marginBottom: '1.5rem', textAlign: 'center' }}>
        {isLogin ? 'Sign In' : 'Create Account'}
      </h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        {error && <p style={{ color: '#ff6b6b', fontSize: '0.9rem' }}>{error}</p>}
        <button type="submit">{isLogin ? 'Sign In' : 'Register'}</button>
      </form>
      <p
        style={{ color: '#888', textAlign: 'center', marginTop: '1rem', cursor: 'pointer' }}
        onClick={() => { setIsLogin(!isLogin); setError(''); }}
      >
        {isLogin ? "Don't have an account? Register" : 'Already have an account? Sign In'}
      </p>
    </div>
  );
}

export default AuthForm;
