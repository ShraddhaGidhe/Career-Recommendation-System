import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import type { RecommendationResult } from '../types';
import { History, Target, ArrowRight } from 'lucide-react';

export const HistoryPage: React.FC = () => {
  const [history, setHistory] = useState<RecommendationResult[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/recommend/history');
        setHistory(response.data.history || []);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  if (loading) return <div className="container text-center mt-4">Loading history...</div>;

  return (
    <div className="container" style={{ maxWidth: '1200px' }}>
      <div className="flex items-center gap-2 mb-4">
        <History size={28} color="var(--primary)" />
        <h1 className="page-title" style={{ marginBottom: 0 }}>Recommendation History</h1>
      </div>

      {history.length === 0 ? (
        <div className="glass-card text-center py-8">
          <p style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>No history found.</p>
          <Link to="/recommend" className="btn-primary">Get Your First Recommendation</Link>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {history.map((item, index) => (
            <div key={item.id} className="glass-card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '0.5rem' }}>
                  <h3 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--primary)' }}>
                    {item.predicted_career}
                  </h3>
                  <span className="badge badge-blue">{item.confidence.toFixed(1)}% Match</span>
                  {index === 0 && <span className="badge badge-green">Latest</span>}
                </div>
                <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem', marginBottom: '0.5rem' }}>
                  Date: {new Date(item.created_at || '').toLocaleString()}
                </p>
                <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                  {item.top_matches.slice(1, 4).map(m => (
                    <span key={m.career} className="badge" style={{ backgroundColor: 'var(--border)' }}>
                      Also matched: {m.career} ({m.confidence.toFixed(0)}%)
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <Link to={`/roadmap/${encodeURIComponent(item.predicted_career)}`} className="btn-secondary flex justify-center align-center" style={{ padding: '0.75rem', borderRadius: '50%' }}>
                  <ArrowRight size={24} color="var(--primary)" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
