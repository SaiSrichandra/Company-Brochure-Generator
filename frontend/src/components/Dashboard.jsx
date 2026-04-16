import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';

const API_BASE_URL = import.meta.env.VITE_API_URL;

function Dashboard({ onBack }) {
  const [brochures, setBrochures] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('token');

  useEffect(() => {
    fetchBrochures();
  }, []);

  const fetchBrochures = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE_URL}/dashboard/brochures`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (res.ok) setBrochures(await res.json());
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Delete this brochure?')) return;
    await fetch(`${API_BASE_URL}/dashboard/brochures/${id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` },
    });
    setBrochures((prev) => prev.filter((b) => b.id !== id));
    if (selected?.id === id) setSelected(null);
  };

  if (selected) {
    return (
      <div className="container">
        <button className="btn-secondary" onClick={() => setSelected(null)}>
          ← Back to Dashboard
        </button>
        <h2 style={{ color: '#fff', margin: '1rem 0' }}>{selected.company_name}</h2>
        <p style={{ color: '#888', fontSize: '0.85rem', marginBottom: '1rem' }}>
          {selected.url} &middot; {new Date(selected.created_at).toLocaleDateString()}
        </p>
        <div className="react-markdown">
          <ReactMarkdown>{selected.markdown}</ReactMarkdown>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h2 style={{ color: '#fff' }}>Saved Brochures</h2>
        <button className="btn-secondary" onClick={onBack}>
          ← Generate New
        </button>
      </div>
      {loading ? (
        <p style={{ color: '#888', textAlign: 'center' }}>Loading...</p>
      ) : brochures.length === 0 ? (
        <p style={{ color: '#888', textAlign: 'center' }}>No saved brochures yet. Generate one!</p>
      ) : (
        <div className="brochure-list">
          {brochures.map((b) => (
            <div key={b.id} className="brochure-card">
              <div
                style={{ cursor: 'pointer', flex: 1 }}
                onClick={() => setSelected(b)}
              >
                <h3 style={{ color: '#fff', marginBottom: '0.25rem' }}>{b.company_name}</h3>
                <p style={{ color: '#888', fontSize: '0.85rem' }}>
                  {new Date(b.created_at).toLocaleDateString()}
                </p>
              </div>
              <button
                className="btn-delete"
                onClick={() => handleDelete(b.id)}
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Dashboard;
