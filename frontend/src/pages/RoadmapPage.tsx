import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import type { RoadmapData } from '../types';
import { Download, CheckCircle, Circle, PlayCircle, BookOpen, Briefcase, TrendingUp } from 'lucide-react';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

export const RoadmapPage: React.FC = () => {
  const { career } = useParams<{ career: string }>();
  const [data, setData] = useState<RoadmapData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRoadmap();
  }, [career]);

  const fetchRoadmap = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/roadmap/${encodeURIComponent(career || '')}`);
      setData(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const updateStatus = async (skill: string, status: string) => {
    try {
      await axios.post('http://localhost:5000/api/roadmap/progress/update', {
        career_name: career,
        skill_name: skill,
        status
      });
      fetchRoadmap(); // Refresh to get updated %
    } catch (err) {
      console.error(err);
    }
  };

  const exportPDF = () => {
    const input = document.getElementById('roadmap-content');
    if (!input) return;
    
    html2canvas(input, { 
      scale: 2,
      onclone: (clonedDoc) => {
        // Fix gradient text issue in html2canvas
        const titles = clonedDoc.querySelectorAll('.page-title');
        titles.forEach((title) => {
          (title as HTMLElement).style.background = 'none';
          (title as HTMLElement).style.color = '#4f46e5';
          (title as HTMLElement).style.webkitTextFillColor = '#4f46e5';
        });
      }
    }).then((canvas) => {
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const padding = 10; // 10mm padding from left and right
      const imgWidth = pdfWidth - 2 * padding;
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      
      pdf.addImage(imgData, 'PNG', padding, padding, imgWidth, imgHeight);
      pdf.save(`${career}-Roadmap.pdf`);
    });
  };

  if (loading) return <div className="container text-center mt-4">Loading roadmap...</div>;
  if (!data) return <div className="container text-center mt-4">Roadmap not found.</div>;

  return (
    <div className="container" id="roadmap-content">
      <div className="flex items-center justify-between mb-4">
        <h1 className="page-title" style={{ marginBottom: 0 }}>{data.career} Roadmap</h1>
        <button onClick={exportPDF} data-html2canvas-ignore="true" className="btn-secondary flex items-center gap-2">
          <Download size={18} /> Export PDF
        </button>
      </div>

      <div>
        {/* Career Summary Card */}
        <div className="glass-card mb-4" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
          <div>
            <h3 className="flex items-center gap-2 mb-2" style={{ color: 'var(--text-muted)' }}><Briefcase size={18} /> Salary Range</h3>
            <p style={{ fontSize: '1.25rem', fontWeight: 600 }}>{data.career_info.salary_range}</p>
          </div>
          <div>
            <h3 className="flex items-center gap-2 mb-2" style={{ color: 'var(--text-muted)' }}><TrendingUp size={18} /> Demand</h3>
            <p style={{ fontSize: '1.25rem', fontWeight: 600, color: data.career_info.demand_color }}>{data.career_info.demand}</p>
          </div>
          <div style={{ gridColumn: '1 / -1' }}>
            <h3 className="mb-2" style={{ color: 'var(--text-muted)' }}>Top Companies Hiring</h3>
            <div className="flex gap-2" style={{ flexWrap: 'wrap' }}>
              {data.career_info.top_companies.map(c => (
                <span key={c} className="badge badge-blue">{c}</span>
              ))}
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="glass-card mb-4">
          <div className="flex items-center justify-between mb-2">
            <h3 style={{ fontWeight: 600 }}>Overall Progress</h3>
            <span style={{ fontWeight: 700, color: 'var(--primary)' }}>{data.progress_pct}%</span>
          </div>
          <div style={{ width: '100%', height: '12px', backgroundColor: 'var(--border)', borderRadius: '999px', overflow: 'hidden' }}>
            <div style={{ width: `${data.progress_pct}%`, height: '100%', backgroundColor: 'var(--primary)', transition: 'width 0.5s ease' }}></div>
          </div>
          <p className="mt-2 text-center" style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>
            {data.completed} of {data.total} skills completed
          </p>
        </div>

        {/* Interactive Skill Checklist */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginTop: '1rem', marginBottom: '0.5rem' }}>Learning Checklist</h2>
          
          {data.roadmap.map((item, idx) => (
            <div key={idx} className="glass-card" style={{ display: 'flex', gap: '1.5rem', alignItems: 'flex-start' }}>
              
              {/* Status Toggle Button */}
              <button 
                onClick={() => {
                  const nextStatus = item.status === 'Not Started' ? 'Learning' : item.status === 'Learning' ? 'Completed' : 'Not Started';
                  updateStatus(item.skill, nextStatus);
                }}
                style={{ marginTop: '0.25rem' }}
              >
                {item.status === 'Completed' ? <CheckCircle size={28} color="var(--secondary)" /> :
                 item.status === 'Learning' ? <PlayCircle size={28} color="var(--primary)" /> :
                 <Circle size={28} color="var(--text-muted)" />}
              </button>
              
              <div style={{ flex: 1 }}>
                <div className="flex items-center gap-4 mb-2">
                  <h3 style={{ fontSize: '1.25rem', fontWeight: 600, color: item.status === 'Completed' ? 'var(--text-muted)' : 'var(--text-main)'}}>
                    {item.skill}
                  </h3>
                  <span className={`badge ${item.priority === 'Essential' ? 'badge-red' : item.priority === 'High' ? 'badge-yellow' : 'badge-blue'}`}>
                    {item.priority}
                  </span>
                  <span style={{ fontSize: '0.875rem', fontWeight: 500, color: item.status === 'Completed' ? 'var(--secondary)' : item.status === 'Learning' ? 'var(--primary)' : 'var(--text-muted)' }}>
                    {item.status}
                  </span>
                </div>
                
                {/* Course Links */}
                {/* {item.courses.length > 0 && (
                  <div style={{ display: 'flex justify-center', gap: '1rem', flexWrap: 'wrap', marginTop: '1rem' }}>
                    {item.courses.map((course, cIdx) => (
                      <a 
                        key={cIdx} 
                        href={course.url} 
                        target="_blank" 
                        rel="noreferrer"
                        className="flex justify-center items-center gap-1"
                        style={{ fontSize: '0.875rem', padding: '0.5rem 1rem', backgroundColor: '#f1f5f9', borderRadius: 'var(--radius-md)', color: 'var(--primary)', fontWeight: 500, border: '1px solid var(--border)' }}
                      >
                        <BookOpen size={16} /> {course.name}
                      </a>
                    ))}
                  </div>
                )} */}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
