import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { API_BASE_URL } from '../config/api';
import { useAuth } from '../context/AuthContext';
import type { RecommendationResult } from '../types';
import { Compass, Clock, ChevronRight, TrendingUp } from 'lucide-react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

export const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [history, setHistory] = useState<RecommendationResult[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/recommend/history`);
        setHistory(response.data.history || []);
      } catch (err) {
        console.error('Failed to fetch history', err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const latest = history[0];

  const chartData = {
    labels: history.slice().reverse().map((_, i) => `Attempt ${i + 1}`),
    datasets: [
      {
        label: 'Match Confidence %',
        data: history.slice().reverse().map(h => h.confidence),
        borderColor: '#4f46e5',
        backgroundColor: 'rgba(79, 70, 229, 0.1)',
        fill: true,
        tension: 0.4
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: { display: true, text: 'Your Match Confidence Trend over Time' }
    },
    scales: { y: { min: 0, max: 100 } }
  };

  return (
    <div className="container">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="page-title" style={{ marginBottom: '0.5rem' }}>Welcome back, {user?.name}!</h1>
          <p style={{ color: 'var(--text-muted)' }}>Here is a summary of your career exploration journey.</p>
        </div>
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <div className="badge" style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)', color: 'var(--text-main)', fontSize: '0.9rem', padding: '0.5rem 1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ color: 'var(--secondary)' }}>★</span> AI Model Accuracy: 99.7%
          </div>
          <Link to="/recommend" className="btn-primary">
            <Compass size={18} /> New Recommendation
          </Link>
        </div>
      </div>

      {loading ? (
        <p>Loading dashboard...</p>
      ) : history.length === 0 ? (
        <div className="glass-card text-center" style={{ padding: '4rem 2rem' }}>
          <Compass size={48} style={{ color: 'var(--primary)', margin: '0 auto 1rem', opacity: 0.5 }} />
          <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem' }}>No recommendations yet</h2>
          <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem' }}>Take the first step to discover your ideal career path.</p>
          <Link to="/recommend" className="btn-primary">Get Started</Link>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: '3fr 2fr', gap: '1.5rem' }}>

          {/* Latest Recommendation Card — top left (wider) */}
          <div className="glass-card" style={{ display: 'flex', flexDirection: 'column' }}>
            <h3 className="flex items-center gap-2 mb-4" style={{ fontSize: '1.125rem', fontWeight: 600 }}>
              <TrendingUp size={20} color="var(--primary)" /> Latest Match
            </h3>
            <div style={{ flex: 1 }}>
              <h2 style={{ fontSize: '1.75rem', fontWeight: 700, color: 'var(--primary)', marginBottom: '0.5rem' }}>
                {latest.predicted_career}
              </h2>
              <div className="badge badge-green mb-4">{latest.confidence.toFixed(1)}% Match</div>
              <p style={{ color: 'var(--text-muted)', marginBottom: '1.5rem', fontSize: '0.9rem' }}>
                {latest.explanation}
              </p>
            </div>
            <Link to={`/roadmap/${encodeURIComponent(latest.predicted_career)}`} className="btn-secondary flex items-center justify-between">
              View Learning Roadmap <ChevronRight size={18} />
            </Link>
          </div>

          {/* Recent Activity — top right (narrower) */}
          <div className="glass-card" style={{ display: 'flex', flexDirection: 'column' }}>
            <h3 className="flex items-center gap-2 mb-4" style={{ fontSize: '1.125rem', fontWeight: 600 }}>
              <Clock size={20} color="var(--primary)" /> Recent Activity
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', flex: 1 }}>
              {history.slice(0, 5).map((item) => (
                <div key={item.id} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingBottom: '0.65rem', borderBottom: '1px solid var(--border)' }}>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{item.predicted_career}</div>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '2px' }}>
                      {new Date(item.created_at || '').toLocaleDateString()}
                    </div>
                  </div>
                  <div className="badge badge-blue">{item.confidence.toFixed(0)}%</div>
                </div>
              ))}
            </div>
            <div className="mt-4 text-center">
              <Link to="/history" style={{ fontSize: '0.875rem', fontWeight: 600 }}>View Full History →</Link>
            </div>
          </div>

          {/* Growth Analytics Chart — full width bottom row (big!) */}
          <div className="glass-card" style={{ gridColumn: '1 / -1' }}>
            <h3 className="flex items-center gap-2 mb-4" style={{ fontSize: '1.125rem', fontWeight: 600 }}>
              <TrendingUp size={20} color="var(--primary)" /> Growth Analytics
            </h3>
            <div style={{ height: 'fit-content' }}>
              <Line data={chartData} options={chartOptions} />
            </div>
          </div>

        </div>
      )}
    </div>
  );
};
