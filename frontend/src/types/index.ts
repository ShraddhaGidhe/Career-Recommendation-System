export interface User {
  id: number;
  name: string;
  email: string;
  created_at?: string;
}

export interface CareerInfo {
  demand: string;
  demand_color: string;
  salary_range: string;
  growth: string;
  top_companies: string[];
  description: string;
  required_skills: string[];
}

export interface TopMatch {
  career: string;
  confidence: number;
}

export interface RecommendationResult {
  id: number;
  predicted_career: string;
  confidence: number;
  top_matches: TopMatch[];
  matched_skills: string[];
  missing_skills: string[];
  explanation: string;
  career_info: CareerInfo;
  created_at?: string;
}

export interface RoadmapSkill {
  skill: string;
  priority: string;
  status: 'Not Started' | 'Learning' | 'Completed';
  courses: { name: string; url: string }[];
}

export interface RoadmapData {
  career: string;
  career_info: CareerInfo;
  roadmap: RoadmapSkill[];
  progress_pct: number;
  completed: number;
  total: number;
}
