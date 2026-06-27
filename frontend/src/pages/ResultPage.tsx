import React from 'react';
import { useLocation, Navigate, Link } from 'react-router-dom';
import type { RecommendationResult } from '../types';
import { Target, CheckCircle2, XCircle, ArrowRight, TrendingUp } from 'lucide-react';

export const ResultPage: React.FC = () => {
  const location = useLocation();
  const result: RecommendationResult = location.state?.result;

  if (!result) {
    return <Navigate to="/recommend" replace />;
  }

  return (
    <div className="container">
      <div className="text-center mb-4">
        <h1 className="page-title" style={{ marginBottom: '0.5rem' }}>Your Best Career Match</h1>
        <p style={{ color: 'var(--text-muted)' }}>Based on your skills, education, and interests.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '2rem', maxWidth: '900px', margin: '0 auto' }}>
        
        {/* Top Result Card */}
        <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', background: 'linear-gradient(to bottom right, var(--surface), #f8fafc)' }}>
          <div style={{ width: '120px', height: '120px', borderRadius: '50%', border: `8px solid var(--primary)`, display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '1.5rem', boxShadow: 'var(--shadow-lg)' }}>
            <span style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--primary)' }}>
              {result.confidence.toFixed(0)}%
            </span>
          </div>
          
          <h2 style={{ fontSize: '2.5rem', fontWeight: 800, color: 'var(--text-main)', marginBottom: '1rem' }}>
            {result.predicted_career}
          </h2>
          
          <p style={{ fontSize: '1.125rem', color: 'var(--text-muted)', maxWidth: '600px', marginBottom: '2rem' }}>
            {result.explanation}
          </p>

          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', justifyContent: 'center' }}>
            <Link to={`/roadmap/${encodeURIComponent(result.predicted_career)}`} className="btn-primary" style={{ padding: '1rem 2rem', fontSize: '1.125rem' }}>
              <Target size={20} /> View Learning Roadmap
            </Link>
          </div>
        </div>

        {/* Skill Gap Analysis */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>
          <div className="glass-card">
            <h3 className="flex items-center gap-2 mb-4" style={{ fontSize: '1.25rem', fontWeight: 600 }}>
              <CheckCircle2 color="var(--secondary)" /> Matched Skills
            </h3>
            {result.matched_skills.length > 0 ? (
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {result.matched_skills.map(s => (
                  <li key={s} className="flex items-center gap-2"><div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--secondary)' }}></div>{s}</li>
                ))}
              </ul>
            ) : (
              <p style={{ color: 'var(--text-muted)' }}>No direct skill matches found for this role yet.</p>
            )}
          </div>
          
          <div className="glass-card">
            <h3 className="flex items-center gap-2 mb-4" style={{ fontSize: '1.25rem', fontWeight: 600 }}>
              <XCircle color="var(--error)" /> Missing Skills to Learn
            </h3>
            {result.missing_skills.length > 0 ? (
              <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {result.missing_skills.map(s => (
                  <li key={s} className="flex items-center gap-2"><div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--error)' }}></div>{s}</li>
                ))}
              </ul>
            ) : (
              <p style={{ color: 'var(--text-muted)' }}>You have all the core skills for this role!</p>
            )}
          </div>
        </div>

        {/* Alternative Careers */}
        <div className="glass-card">
          <h3 className="flex items-center gap-2 mb-4" style={{ fontSize: '1.25rem', fontWeight: 600 }}>
            <TrendingUp color="var(--primary)" /> Other Strong Matches
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            {result.top_matches.slice(1).map((match, i) => (
              <div key={i} style={{ padding: '1rem', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontWeight: 500 }}>{match.career}</span>
                <span className="badge badge-blue">{match.confidence.toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
};
