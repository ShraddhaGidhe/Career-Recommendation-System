import React from 'react';
import { Link, Navigate } from 'react-router-dom';
import { Sparkles, Target, TrendingUp, BookOpen, Compass } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import heroImg from '../assets/20944398.png';

export const Landing: React.FC = () => {
  const { isAuthenticated } = useAuth();

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%' }}>

      {/* ── Hero Section ──────────────────────────────────── */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: '3rem',
        width: '100%',
        maxWidth: '1100px',
        minHeight: '60vh',
        padding: '1.5rem 2rem',
        flexWrap: 'wrap',
      }}>

        {/* Left: Text + Buttons */}
        <div style={{ flex: '1 1 420px', textAlign: 'left' }}>

          {/* Badge */}
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: '0.5rem',
            background: 'rgba(170,59,255,0.1)', border: '1px solid rgba(170,59,255,0.3)',
            borderRadius: '99px', padding: '0.4rem 1rem', marginBottom: '1.5rem',
            fontSize: '0.85rem', color: '#aa3bff', fontWeight: 600,
          }}>
            <Compass size={14} /> AI-Powered Career Guidance
          </div>

          <h1 style={{
            fontSize: 'clamp(2rem, 5vw, 3.2rem)', fontWeight: 800,
            lineHeight: 1.15, marginBottom: '1.25rem', letterSpacing: '-1px',
            background: 'linear-gradient(120deg, #aa3bff 0%, #ff3b9a 100%)',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
          }}>
            Discover Your<br />True Career Path
          </h1>

          <p style={{
            fontSize: '1.1rem', color: 'var(--text-muted, #6b6375)',
            lineHeight: 1.7, marginBottom: '2.5rem', maxWidth: '480px',
          }}>
            Our <strong>Random Forest ML engine</strong> analyzes your skills, education,
            and interests across <strong>50+ career options</strong> to find your perfect
            fit — instantly.
          </p>

          <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
            <Link to="/register" style={{
              padding: '0.9rem 2rem', fontSize: '1rem',
              display: 'inline-flex', alignItems: 'center', gap: '0.5rem',
              borderRadius: '99px',
              background: 'linear-gradient(135deg, #aa3bff, #ff3b9a)',
              color: 'white', textDecoration: 'none', fontWeight: 700,
              boxShadow: '0 4px 20px rgba(170,59,255,0.35)',
            }}>
              <Sparkles size={18} /> Get Started — It's Free
            </Link>
            <Link to="/login" style={{
              padding: '0.9rem 2rem', fontSize: '1rem',
              display: 'inline-flex', alignItems: 'center', gap: '0.5rem',
              borderRadius: '99px', border: '2px solid #aa3bff',
              color: '#aa3bff', textDecoration: 'none', fontWeight: 700,
              background: 'transparent',
            }}>
              Sign In
            </Link>
          </div>

          {/* Stats Row */}
          <div style={{ display: 'flex', gap: '2.5rem', marginTop: '1.5rem', flexWrap: 'wrap' }}>
            {[['50+', 'Career Options'], ['5,000+', 'Training Samples'], ['125+', 'Skills Mapped']].map(([num, label]) => (
              <div key={label}>
                <div style={{ fontSize: '1.6rem', fontWeight: 800, color: '#aa3bff' }}>{num}</div>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted, #6b6375)', fontWeight: 500 }}>{label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Hero Image */}
        <div style={{ flex: '1 1 380px', display: 'flex', justifyContent: 'center' }}>
          {/* <div style={{
            borderRadius: '24px',
            overflow: 'hidden',
            boxShadow: '0 25px 60px rgba(170,59,255,0.25)',
            border: '3px solid rgba(170,59,255,0.2)',
            maxWidth: '460px',
            width: '100%',
          }}> */}
            <img
              src={heroImg}
              alt="Career Guidance Illustration"
              style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block',filter:"drop-shadow(0 25px 60px rgba(170,59,255,0.35))" }}
            />
          {/* </div> */}
        </div>
      </div>

      {/* ── Feature Cards ─────────────────────────────────── */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
        gap: '1.5rem',
        width: '100%', maxWidth: '1100px',
        padding: '0 2rem 4rem',
      }}>
        {[
          {
            icon: <Target size={28} color="#aa3bff" />,
            title: 'Personalized Matching',
            desc: 'Random Forest ML analyzes your full profile across hundreds of skill combinations.',
          },
          {
            icon: <TrendingUp size={28} color="#aa3bff" />,
            title: 'Interactive Roadmaps',
            desc: 'Get step-by-step learning paths to bridge skill gaps for your dream career.',
          },
          {
            icon: <BookOpen size={28} color="#aa3bff" />,
            title: 'Track Your Progress',
            desc: 'Mark skills as completed and monitor your career readiness over time.',
          },
        ].map(({ icon, title, desc }) => (
          <div key={title} style={{
            padding: '1.75rem', borderRadius: '16px',
            background: 'var(--bg, #fff)',
            border: '1px solid var(--border, #eee)',
            boxShadow: '0 4px 20px rgba(0,0,0,0.06)',
            textAlign: 'left',
          }}>
            <div className="flex gap-2" style={{ marginBottom: '1rem' }}>
              <div>{icon}</div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: '0.5rem', color: 'var(--text-h, #08060d)' }}>{title}</h3>
            </div>
            <p style={{ color: 'var(--text-muted, #6b6375)', fontSize: '0.9rem', lineHeight: 1.6 }}>{desc}</p>
          </div>
        ))}
      </div>

    </div>
  );
};
