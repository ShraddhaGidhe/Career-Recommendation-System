import pandas as pd
import numpy as np
import random
import os

careers_definitions = [
    # Tech / IT
    {"name": "Software Engineer", "edu": ["B.Tech", "B.Sc", "M.Tech"], "spec": ["Computer Science", "Information Technology"], "skills": ["Python", "Java", "C++", "SQL"], "interest": "Coding"},
    {"name": "Data Scientist", "edu": ["B.Tech", "M.Tech", "M.Sc"], "spec": ["Computer Science", "Data Science", "Statistics"], "skills": ["Python", "Machine Learning", "SQL", "Statistics", "R"], "interest": "Data Analysis"},
    {"name": "Cloud Architect", "edu": ["B.Tech", "M.Tech"], "spec": ["Computer Science", "Information Technology"], "skills": ["AWS", "Azure", "Linux", "Networking"], "interest": "Infrastructure"},
    {"name": "Cyber Security Analyst", "edu": ["B.Tech", "B.Sc"], "spec": ["Cyber Security", "Computer Science", "Information Technology"], "skills": ["Networking", "Linux", "Ethical Hacking", "Cryptography"], "interest": "Security"},
    {"name": "DevOps Engineer", "edu": ["B.Tech"], "spec": ["Computer Science", "Information Technology"], "skills": ["Linux", "Docker", "Kubernetes", "CI/CD"], "interest": "Automation"},
    {"name": "UI/UX Designer", "edu": ["B.Des", "B.Tech", "B.A"], "spec": ["Design", "Computer Science", "Fine Arts"], "skills": ["Figma", "Prototyping", "User Research", "Adobe XD"], "interest": "Design"},
    {"name": "Mobile App Developer", "edu": ["B.Tech", "B.Sc", "BCA"], "spec": ["Computer Science", "Information Technology"], "skills": ["Java", "Kotlin", "Swift", "Flutter", "React Native"], "interest": "Mobile Development"},
    {"name": "Game Developer", "edu": ["B.Tech", "B.Sc"], "spec": ["Computer Science", "Game Design"], "skills": ["C#", "C++", "Unity", "Unreal Engine"], "interest": "Gaming"},
    {"name": "Blockchain Developer", "edu": ["B.Tech", "M.Tech"], "spec": ["Computer Science", "Information Technology"], "skills": ["Solidity", "Cryptography", "C++", "JavaScript"], "interest": "Web3"},
    {"name": "AI/ML Engineer", "edu": ["B.Tech", "M.Tech"], "spec": ["Computer Science", "Artificial Intelligence"], "skills": ["Python", "Deep Learning", "TensorFlow", "PyTorch"], "interest": "Artificial Intelligence"},
    {"name": "Database Administrator", "edu": ["B.Tech", "B.Sc", "BCA"], "spec": ["Computer Science", "Information Technology"], "skills": ["SQL", "Oracle", "MySQL", "Database Management"], "interest": "Data Management"},
    {"name": "Network Engineer", "edu": ["B.Tech", "Diploma"], "spec": ["Computer Science", "Electronics"], "skills": ["Networking", "Cisco", "TCP/IP", "Linux"], "interest": "Networking"},
    {"name": "IT Support Specialist", "edu": ["B.Sc", "BCA", "Diploma"], "spec": ["Information Technology", "Computer Science"], "skills": ["Troubleshooting", "Windows", "Linux", "Hardware"], "interest": "Tech Support"},
    {"name": "Systems Analyst", "edu": ["B.Tech", "MCA"], "spec": ["Computer Science", "Information Systems"], "skills": ["System Design", "SQL", "Business Analysis", "Java"], "interest": "Systems Analysis"},
    {"name": "Front-End Developer", "edu": ["B.Tech", "B.Sc", "BCA"], "spec": ["Computer Science", "Information Technology"], "skills": ["HTML", "CSS", "JavaScript", "React", "Vue"], "interest": "Web Development"},
    {"name": "Back-End Developer", "edu": ["B.Tech", "MCA"], "spec": ["Computer Science", "Information Technology"], "skills": ["Python", "Java", "Node.js", "SQL", "API Design"], "interest": "Web Development"},
    {"name": "Full Stack Developer", "edu": ["B.Tech", "MCA"], "spec": ["Computer Science", "Information Technology"], "skills": ["JavaScript", "React", "Node.js", "SQL", "MongoDB"], "interest": "Web Development"},
    {"name": "QA Tester", "edu": ["B.Tech", "BCA", "B.Sc"], "spec": ["Computer Science", "Information Technology"], "skills": ["Testing", "Selenium", "Java", "Python"], "interest": "Quality Assurance"},
    
    # Business & Management
    {"name": "Product Manager", "edu": ["MBA", "B.Tech"], "spec": ["Management", "Computer Science", "Business"], "skills": ["Agile", "Leadership", "Market Research", "Data Analysis"], "interest": "Product Management"},
    {"name": "Business Analyst", "edu": ["MBA", "BBA", "B.Com"], "spec": ["Business Analytics", "Finance", "Management"], "skills": ["Excel", "SQL", "Data Analysis", "Communication"], "interest": "Business Analysis"},
    {"name": "Marketing Manager", "edu": ["MBA", "BBA"], "spec": ["Marketing", "Management"], "skills": ["Digital Marketing", "SEO", "Communication", "Content Strategy"], "interest": "Marketing"},
    {"name": "Financial Analyst", "edu": ["MBA", "B.Com", "CA"], "spec": ["Finance", "Accounting"], "skills": ["Financial Modeling", "Excel", "Accounting", "Valuation"], "interest": "Finance"},
    {"name": "HR Manager", "edu": ["MBA", "BBA", "BA"], "spec": ["Human Resources", "Management", "Psychology"], "skills": ["Recruitment", "Communication", "Employee Relations", "HRIS"], "interest": "Human Resources"},
    {"name": "Sales Manager", "edu": ["MBA", "BBA", "Any Degree"], "spec": ["Marketing", "Management", "Any"], "skills": ["Sales", "Negotiation", "CRM", "Communication"], "interest": "Sales"},
    {"name": "Operations Manager", "edu": ["MBA", "B.Tech"], "spec": ["Operations", "Management", "Mechanical"], "skills": ["Logistics", "Process Optimization", "Leadership", "Supply Chain"], "interest": "Operations"},
    {"name": "Supply Chain Analyst", "edu": ["BBA", "B.Tech", "MBA"], "spec": ["Supply Chain", "Logistics", "Operations"], "skills": ["Data Analysis", "Logistics", "Excel", "Procurement"], "interest": "Supply Chain"},
    {"name": "Digital Marketer", "edu": ["BBA", "B.A", "B.Com"], "spec": ["Marketing", "Mass Communication"], "skills": ["SEO", "Social Media", "Google Ads", "Content Creation"], "interest": "Digital Marketing"},
    {"name": "Accountant", "edu": ["B.Com", "M.Com", "CA"], "spec": ["Accounting", "Finance"], "skills": ["Tally", "Accounting", "Taxation", "Excel"], "interest": "Accounting"},
    
    # Engineering (Non-IT)
    {"name": "Mechanical Engineer", "edu": ["B.Tech", "M.Tech"], "spec": ["Mechanical Engineering"], "skills": ["AutoCAD", "Thermodynamics", "SolidWorks", "Manufacturing"], "interest": "Mechanical Systems"},
    {"name": "Civil Engineer", "edu": ["B.Tech", "M.Tech"], "spec": ["Civil Engineering"], "skills": ["AutoCAD", "Structural Analysis", "Project Management", "Surveying"], "interest": "Construction"},
    {"name": "Electrical Engineer", "edu": ["B.Tech", "M.Tech"], "spec": ["Electrical Engineering"], "skills": ["Circuit Design", "Power Systems", "AutoCAD Electrical", "Electronics"], "interest": "Electrical Systems"},
    {"name": "Electronics Engineer", "edu": ["B.Tech", "M.Tech"], "spec": ["Electronics and Communication"], "skills": ["VLSI", "Embedded Systems", "Circuit Design", "Microcontrollers"], "interest": "Electronics"},
    {"name": "Chemical Engineer", "edu": ["B.Tech", "M.Tech"], "spec": ["Chemical Engineering"], "skills": ["Process Engineering", "Thermodynamics", "Chemistry", "Safety Protocols"], "interest": "Chemical Processes"},
    {"name": "Aerospace Engineer", "edu": ["B.Tech", "M.Tech"], "spec": ["Aerospace Engineering"], "skills": ["Aerodynamics", "Propulsion", "CAD", "Fluid Mechanics"], "interest": "Aerospace"},
    {"name": "Biomedical Engineer", "edu": ["B.Tech", "M.Tech"], "spec": ["Biomedical Engineering"], "skills": ["Medical Devices", "Biomechanics", "Signal Processing", "Anatomy"], "interest": "Healthcare Tech"},
    
    # Healthcare & Science
    {"name": "Doctor (MBBS)", "edu": ["MBBS"], "spec": ["Medicine"], "skills": ["Patient Care", "Diagnosis", "Anatomy", "Pharmacology"], "interest": "Healthcare"},
    {"name": "Nurse", "edu": ["B.Sc Nursing", "GNM"], "spec": ["Nursing"], "skills": ["Patient Care", "First Aid", "Empathy", "Clinical Skills"], "interest": "Healthcare"},
    {"name": "Pharmacist", "edu": ["B.Pharm", "M.Pharm"], "spec": ["Pharmacy"], "skills": ["Pharmacology", "Drug Dispensing", "Chemistry", "Healthcare"], "interest": "Pharmacy"},
    {"name": "Physiotherapist", "edu": ["BPT", "MPT"], "spec": ["Physiotherapy"], "skills": ["Rehabilitation", "Anatomy", "Patient Care", "Exercise Therapy"], "interest": "Rehabilitation"},
    {"name": "Clinical Researcher", "edu": ["B.Sc", "M.Sc", "B.Pharm"], "spec": ["Biotechnology", "Life Sciences", "Pharmacy"], "skills": ["Clinical Trials", "Data Collection", "Research", "Regulatory Affairs"], "interest": "Research"},
    {"name": "Microbiologist", "edu": ["B.Sc", "M.Sc"], "spec": ["Microbiology", "Biotechnology"], "skills": ["Lab Techniques", "Microscopy", "Research", "Data Analysis"], "interest": "Biology"},
    {"name": "Environmental Scientist", "edu": ["B.Sc", "M.Sc"], "spec": ["Environmental Science"], "skills": ["Data Analysis", "Research", "Ecology", "GIS"], "interest": "Environment"},
    
    # Arts, Media & Design
    {"name": "Graphic Designer", "edu": ["BFA", "B.Des", "BA"], "spec": ["Fine Arts", "Visual Arts", "Design"], "skills": ["Adobe Illustrator", "Photoshop", "Typography", "Creativity"], "interest": "Graphic Design"},
    {"name": "Content Writer", "edu": ["BA", "MA", "B.Com"], "spec": ["English", "Journalism", "Mass Communication"], "skills": ["Writing", "Editing", "SEO", "Research"], "interest": "Writing"},
    {"name": "Journalist", "edu": ["BA", "MA"], "spec": ["Journalism", "Mass Communication"], "skills": ["Reporting", "Writing", "Interviewing", "Research"], "interest": "Journalism"},
    {"name": "Video Editor", "edu": ["BA", "Diploma"], "spec": ["Film Studies", "Mass Communication"], "skills": ["Premiere Pro", "Final Cut Pro", "After Effects", "Creativity"], "interest": "Video Production"},
    {"name": "Interior Designer", "edu": ["B.Des", "B.Arch", "Diploma"], "spec": ["Interior Design", "Architecture"], "skills": ["AutoCAD", "Space Planning", "SketchUp", "Creativity"], "interest": "Interior Design"},
    {"name": "Architect", "edu": ["B.Arch", "M.Arch"], "spec": ["Architecture"], "skills": ["AutoCAD", "Architectural Design", "3D Modeling", "Revit"], "interest": "Architecture"},
    
    # Miscellaneous
    {"name": "Lawyer", "edu": ["LLB", "BA LLB"], "spec": ["Law"], "skills": ["Legal Research", "Argumentation", "Drafting", "Communication"], "interest": "Law"},
    {"name": "Teacher", "edu": ["B.Ed", "BA", "B.Sc"], "spec": ["Education", "Any Subject"], "skills": ["Teaching", "Communication", "Patience", "Lesson Planning"], "interest": "Education"},
]

def generate_dataset(num_rows=5000):
    data = []
    all_certifications = ["AWS Certified", "PMP", "CPA", "CFA", "Google Analytics", "Six Sigma", "Red Hat", "Cisco CCNA", "None"]
    
    for _ in range(num_rows):
        career = random.choice(careers_definitions)
        # Select 2-4 skills appropriate for the career
        num_skills = random.randint(2, len(career["skills"]))
        chosen_skills = random.sample(career["skills"], num_skills)
        
        # Add 1 random noise skill occasionally
        if random.random() > 0.5:
            other_career = random.choice(careers_definitions)
            noise_skill = random.choice(other_career["skills"])
            if noise_skill not in chosen_skills:
                chosen_skills.append(noise_skill)
                
        # Shuffle skills
        random.shuffle(chosen_skills)
        
        row = {
            "Education Level": random.choice(career["edu"]),
            "Specialization": random.choice(career["spec"]),
            "Skills": ", ".join(chosen_skills),
            "Interest": career["interest"],
            "Certifications": random.choice(all_certifications),
            "CGPA": round(random.uniform(6.5, 9.8), 2),
            "Career Options": career["name"]
        }
        data.append(row)
        
    df = pd.DataFrame(data)
    df.to_excel("career_dataset_large.xlsx", index=False)
    print(f"Generated career_dataset_large.xlsx with {len(df)} rows and {len(careers_definitions)} careers.")


def generate_career_data_py():
    print("Generating career_data.py...")
    content = '"""\nAuto-generated career data mapping for 50+ careers\n"""\n\n'
    
    content += "CAREER_INFO = {\n"
    for career in careers_definitions:
        content += f'    "{career["name"]}": {{\n'
        content += f'        "demand": "High",\n'
        content += f'        "demand_color": "var(--secondary)",\n'
        content += f'        "salary_range": "₹4 Lakhs - ₹15 Lakhs",\n'
        content += f'        "growth": "Strong expected growth in India over the next decade.",\n'
        content += f'        "top_companies": ["TCS", "Infosys", "Wipro", "Startups"],\n'
        content += f'        "description": "A dynamic role focused on {career["interest"]}.",\n'
        content += f'        "required_skills": {career["skills"]},\n'
        
        # Generate generic roadmap based on required skills
        roadmap = []
        for i, skill in enumerate(career["skills"]):
            priority = "Essential" if i < 2 else "High"
            roadmap.append({
                "skill": f"Master {skill}",
                "priority": priority,
                "status": "Not Started",
                "courses": [{"name": f"Intro to {skill}", "url": "#"}]
            })
            
        content += f'        "roadmap": {roadmap}\n'
        content += "    },\n"
        
    content += "}\n\n"
    content += "def get_career_data(career_name: str) -> dict:\n"
    content += "    return CAREER_INFO.get(career_name, CAREER_INFO.get('Software Engineer'))\n"
    
    with open("career_data.py", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    generate_dataset()
    generate_career_data_py()
