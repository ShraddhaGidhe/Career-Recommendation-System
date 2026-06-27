import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Compass, Loader } from 'lucide-react';

const EDUCATION_LEVELS = ['Any Degree', 'B.A', 'B.Arch', 'B.Com', 'B.Des', 'B.Ed', 'B.Pharm', 'B.Sc', 'B.Sc Nursing', 'B.Tech', 'BA', 'BA LLB', 'BBA', 'BCA', 'BFA', 'BPT', 'CA', 'Diploma', 'GNM', 'LLB', 'M.Arch', 'M.Com', 'M.Pharm', 'M.Sc', 'M.Tech', 'MA', 'MBA', 'MBBS', 'MCA', 'MPT'];
const SPECIALIZATIONS = ['Accounting', 'Aerospace Engineering', 'Any', 'Any Subject', 'Architecture', 'Artificial Intelligence', 'Biomedical Engineering', 'Biotechnology', 'Business', 'Business Analytics', 'Chemical Engineering', 'Civil Engineering', 'Computer Science', 'Cyber Security', 'Data Science', 'Design', 'Education', 'Electrical Engineering', 'Electronics', 'Electronics and Communication', 'English', 'Environmental Science', 'Film Studies', 'Finance', 'Fine Arts', 'Game Design', 'Human Resources', 'Information Systems', 'Information Technology', 'Interior Design', 'Journalism', 'Law', 'Life Sciences', 'Logistics', 'Management', 'Marketing', 'Mass Communication', 'Mechanical', 'Mechanical Engineering', 'Medicine', 'Microbiology', 'Nursing', 'Operations', 'Pharmacy', 'Physiotherapy', 'Psychology', 'Statistics', 'Supply Chain', 'Visual Arts'];
const INTERESTS = ['Accounting', 'Aerospace', 'Architecture', 'Artificial Intelligence', 'Automation', 'Biology', 'Business Analysis', 'Chemical Processes', 'Coding', 'Construction', 'Data Analysis', 'Data Management', 'Design', 'Digital Marketing', 'Education', 'Electrical Systems', 'Electronics', 'Environment', 'Finance', 'Gaming', 'Graphic Design', 'Healthcare', 'Healthcare Tech', 'Human Resources', 'Infrastructure', 'Interior Design', 'Journalism', 'Law', 'Marketing', 'Mechanical Systems', 'Mobile Development', 'Networking', 'Operations', 'Pharmacy', 'Product Management', 'Quality Assurance', 'Rehabilitation', 'Research', 'Sales', 'Security', 'Supply Chain', 'Systems Analysis', 'Tech Support', 'Video Production', 'Web Development', 'Web3', 'Writing'];
const ALL_SKILLS = [
  '3D Modeling', 'API Design', 'AWS', 'Accounting', 'Adobe Illustrator', 'Adobe XD', 'Aerodynamics', 'After Effects', 'Agile', 'Anatomy', 'Architectural Design', 'Argumentation', 'AutoCAD', 'AutoCAD Electrical', 'Azure', 'Biomechanics', 'Business Analysis', 'C#', 'C++', 'CAD', 'CI/CD', 'CRM', 'CSS', 'Chemistry', 'Circuit Design', 'Cisco', 'Clinical Skills', 'Clinical Trials', 'Communication', 'Content Creation', 'Content Strategy', 'Creativity', 'Cryptography', 'Data Analysis', 'Data Collection', 'Database Management', 'Deep Learning', 'Diagnosis', 'Digital Marketing', 'Docker', 'Drafting', 'Drug Dispensing', 'Ecology', 'Editing', 'Electronics', 'Embedded Systems', 'Empathy', 'Employee Relations', 'Ethical Hacking', 'Excel', 'Exercise Therapy', 'Figma', 'Final Cut Pro', 'Financial Modeling', 'First Aid', 'Fluid Mechanics', 'Flutter', 'GIS', 'Google Ads', 'HRIS', 'HTML', 'Hardware', 'Healthcare', 'Interviewing', 'Java', 'JavaScript', 'Kotlin', 'Kubernetes', 'Lab Techniques', 'Leadership', 'Legal Research', 'Lesson Planning', 'Linux', 'Logistics', 'Machine Learning', 'Manufacturing', 'Market Research', 'Medical Devices', 'Microcontrollers', 'Microscopy', 'MongoDB', 'MySQL', 'Negotiation', 'Networking', 'Node.js', 'Oracle', 'Patience', 'Patient Care', 'Pharmacology', 'Photoshop', 'Power Systems', 'Premiere Pro', 'Process Engineering', 'Process Optimization', 'Procurement', 'Project Management', 'Propulsion', 'Prototyping', 'PyTorch', 'Python', 'R', 'React', 'React Native', 'Recruitment', 'Regulatory Affairs', 'Rehabilitation', 'Reporting', 'Research', 'Revit', 'SEO', 'SQL', 'Safety Protocols', 'Sales', 'Selenium', 'Signal Processing', 'SketchUp', 'Social Media', 'SolidWorks', 'Solidity', 'Space Planning', 'Statistics', 'Structural Analysis', 'Supply Chain', 'Surveying', 'Swift', 'System Design', 'TCP/IP', 'Tally', 'Taxation', 'Teaching', 'TensorFlow', 'Testing', 'Thermodynamics', 'Troubleshooting', 'Typography', 'Unity', 'Unreal Engine', 'User Research', 'VLSI', 'Valuation', 'Vue', 'Windows', 'Writing'
];

export const RecommendForm: React.FC = () => {
  const [formData, setFormData] = useState({
    education: '',
    specialization: '',
    interest: '',
    cgpa: 70
  });
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [skillSearch, setSkillSearch] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedSearch(skillSearch), 300);
    return () => clearTimeout(timer);
  }, [skillSearch]);
  const navigate = useNavigate();

  const handleSkillToggle = (skill: string) => {
    setSelectedSkills(prev => 
      prev.includes(skill) ? prev.filter(s => s !== skill) : [...prev, skill]
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.education || !formData.interest || selectedSkills.length === 0) {
      setError('Please fill all required fields and select at least one skill.');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const payload = {
        education: formData.education,
        specialization: formData.specialization,
        skills: selectedSkills,
        interest: formData.interest,
        certifications: [], // keeping empty for simplicity or add later
        cgpa: formData.cgpa
      };
      
      const response = await axios.post('http://localhost:5000/api/recommend/predict', payload);
      // Pass the result via state to ResultPage
      navigate('/result', { state: { result: response.data } });
    } catch (err: any) {
      setError(err.response?.data?.error || 'Prediction failed');
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ maxWidth: '1200px' }}>
      <h1 className="page-title text-center">Discover Your Career Path</h1>
      
      <div className="glass-card">
        {error && <div style={{ color: 'var(--error)', backgroundColor: '#fef2f2', padding: '1rem', borderRadius: 'var(--radius-md)', marginBottom: '1.5rem' }}>{error}</div>}
        
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
            <div>
              <label className="label">Education Level <span style={{ color: 'red' }}>*</span></label>
              <select 
                className="input-field" 
                value={formData.education} 
                onChange={(e) => setFormData({...formData, education: e.target.value})}
                required
              >
                <option value="">Select Level</option>
                {EDUCATION_LEVELS.map(level => <option key={level} value={level}>{level}</option>)}
              </select>
            </div>
            
            <div>
              <label className="label">Specialization</label>
              <select 
                className="input-field" 
                value={formData.specialization} 
                onChange={(e) => setFormData({...formData, specialization: e.target.value})}
              >
                <option value="">Select Specialization (Optional)</option>
                {SPECIALIZATIONS.map(spec => <option key={spec} value={spec}>{spec}</option>)}
              </select>
            </div>
          </div>

          <div>
            <label className="label">Primary Interest <span style={{ color: 'red' }}>*</span></label>
            <select 
              className="input-field" 
              value={formData.interest} 
              onChange={(e) => setFormData({...formData, interest: e.target.value})}
              required
            >
              <option value="">Select Interest</option>
              {INTERESTS.map(int => <option key={int} value={int}>{int}</option>)}
            </select>
          </div>

          <div>
            <label className="label">CGPA / Percentage</label>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <input 
                type="range" 
                min="0" max="100" 
                value={formData.cgpa} 
                onChange={(e) => setFormData({...formData, cgpa: parseInt(e.target.value)})}
                style={{ flex: 1 }}
              />
              <span style={{ fontWeight: 600, width: '40px' }}>{formData.cgpa}%</span>
            </div>
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <label className="label" style={{ marginBottom: 0 }}>Your Skills <span style={{ color: 'red' }}>*</span> (Select multiple)</label>
              <span style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>{selectedSkills.length} selected</span>
            </div>
            
            <input
              type="text"
              placeholder="Search skills... (e.g. Java, Data)"
              className="input-field"
              value={skillSearch}
              onChange={(e) => setSkillSearch(e.target.value)}
              style={{ marginBottom: '1rem' }}
            />
            
            <div style={{ 
              display: 'flex', flexWrap: 'wrap', gap: '0.5rem', 
              maxHeight: '280px', overflowY: 'auto', 
              padding: '1rem', border: '1px solid var(--border)', 
              borderRadius: 'var(--radius-md)', backgroundColor: 'rgba(0,0,0,0.02)' 
            }}>
              {ALL_SKILLS.filter(skill => skill.toLowerCase().startsWith(debouncedSearch.toLowerCase())).map(skill => {
                const isSelected = selectedSkills.includes(skill);
                return (
                  <button
                    key={skill}
                    type="button"
                    onClick={() => handleSkillToggle(skill)}
                    style={{
                      padding: '0.5rem 1rem',
                      borderRadius: '9999px',
                      border: `1px solid ${isSelected ? 'var(--primary)' : 'var(--border)'}`,
                      backgroundColor: isSelected ? 'var(--primary)' : 'var(--surface)',
                      color: isSelected ? 'white' : 'var(--text-main)',
                      fontSize: '0.875rem',
                      transition: 'all 0.2s',
                      cursor: 'pointer'
                    }}
                  >
                    {skill} {isSelected && '✓'}
                  </button>
                );
              })}
              
              {ALL_SKILLS.filter(skill => skill.toLowerCase().startsWith(debouncedSearch.toLowerCase())).length === 0 && (
                <div style={{ width: '100%', textAlign: 'center', color: 'var(--text-muted)', padding: '1rem 0' }}>
                  No skills found matching "{debouncedSearch}"
                </div>
              )}
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1rem' }}>
            <button type="submit" className="btn-primary" disabled={loading} style={{ fontSize: '1.125rem', padding: '1rem 2rem' }}>
              {loading ? <Loader className="animate-spin" /> : <Compass />}
              {loading ? 'Analyzing Profile...' : 'Get Career Recommendation'}
            </button>
          </div>
          
        </form>
      </div>
    </div>
  );
};
