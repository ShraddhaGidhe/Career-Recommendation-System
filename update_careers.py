import re

def update_career_data():
    with open('backend/ml/career_data.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Define realistic profiles
    profiles = {
        "Tech_High": {
            "demand": "High", "demand_color": "var(--secondary)",
            "salary": "₹8 Lakhs - ₹30 Lakhs",
            "growth": "Exponential growth expected driven by AI and Cloud adoption.",
            "companies": '["Google", "Microsoft", "Amazon", "High-growth Startups"]'
        },
        "Tech_Mid": {
            "demand": "High", "demand_color": "var(--secondary)",
            "salary": "₹5 Lakhs - ₹18 Lakhs",
            "growth": "Consistent high demand across IT and product companies.",
            "companies": '["TCS", "Infosys", "Tech Mahindra", "Startups"]'
        },
        "Tech_Support": {
            "demand": "Stable", "demand_color": "var(--primary)",
            "salary": "₹3 Lakhs - ₹8 Lakhs",
            "growth": "Steady demand but increasing automation risks.",
            "companies": '["Wipro", "HCL", "IBM", "Local IT Firms"]'
        },
        "Medical": {
            "demand": "Very High", "demand_color": "var(--secondary)",
            "salary": "₹8 Lakhs - ₹25 Lakhs+",
            "growth": "Constant high demand due to healthcare needs and population growth.",
            "companies": '["Apollo Hospitals", "Fortis", "AIIMS", "Private Clinics"]'
        },
        "Healthcare_Support": {
            "demand": "High", "demand_color": "var(--secondary)",
            "salary": "₹2.5 Lakhs - ₹8 Lakhs",
            "growth": "Growing demand post-pandemic for specialized care.",
            "companies": '["Sun Pharma", "Cipla", "Max Healthcare", "Local Clinics"]'
        },
        "Business": {
            "demand": "Stable", "demand_color": "var(--primary)",
            "salary": "₹6 Lakhs - ₹22 Lakhs",
            "growth": "Strong need for strategic and operational leadership.",
            "companies": '["McKinsey", "Deloitte", "Goldman Sachs", "Amazon"]'
        },
        "Creative": {
            "demand": "Variable", "demand_color": "var(--primary)",
            "salary": "₹3 Lakhs - ₹12 Lakhs",
            "growth": "High freelance potential and growing digital media needs.",
            "companies": '["Ad Agencies", "Media Houses", "Freelance", "Tech Startups"]'
        },
        "Core_Eng": {
            "demand": "Stable", "demand_color": "var(--primary)",
            "salary": "₹3 Lakhs - ₹12 Lakhs",
            "growth": "Steady growth tied to infrastructure and manufacturing sectors.",
            "companies": '["L&T", "Tata Motors", "BHEL", "Reliance"]'
        },
        "Traditional": {
            "demand": "Stable", "demand_color": "var(--primary)",
            "salary": "₹3 Lakhs - ₹10 Lakhs",
            "growth": "Evergreen professions with consistent societal need.",
            "companies": '["Schools/Universities", "Law Firms", "Government", "Private Practice"]'
        }
    }

    career_mapping = {
        "Data Scientist": "Tech_High", "Cloud Architect": "Tech_High", "AI/ML Engineer": "Tech_High", 
        "Blockchain Developer": "Tech_High", "DevOps Engineer": "Tech_High", "Cyber Security Analyst": "Tech_High",
        "Software Engineer": "Tech_Mid", "Full Stack Developer": "Tech_Mid", "Back-End Developer": "Tech_Mid",
        "Mobile App Developer": "Tech_Mid", "Database Administrator": "Tech_Mid", "Network Engineer": "Tech_Mid",
        "Front-End Developer": "Tech_Mid", "Systems Analyst": "Tech_Mid", "Game Developer": "Tech_Mid",
        "IT Support Specialist": "Tech_Support", "QA Tester": "Tech_Support",
        "Doctor (MBBS)": "Medical",
        "Nurse": "Healthcare_Support", "Pharmacist": "Healthcare_Support", "Physiotherapist": "Healthcare_Support",
        "Clinical Researcher": "Healthcare_Support", "Microbiologist": "Healthcare_Support",
        "Product Manager": "Business", "Business Analyst": "Business", "Financial Analyst": "Business",
        "Marketing Manager": "Business", "HR Manager": "Business", "Sales Manager": "Business",
        "Operations Manager": "Business", "Supply Chain Analyst": "Business", "Digital Marketer": "Business",
        "Accountant": "Business",
        "UI/UX Designer": "Creative", "Graphic Designer": "Creative", "Video Editor": "Creative",
        "Content Writer": "Creative", "Journalist": "Creative", "Interior Designer": "Creative",
        "Mechanical Engineer": "Core_Eng", "Civil Engineer": "Core_Eng", "Electrical Engineer": "Core_Eng",
        "Electronics Engineer": "Core_Eng", "Chemical Engineer": "Core_Eng", "Aerospace Engineer": "Core_Eng",
        "Biomedical Engineer": "Core_Eng", "Environmental Scientist": "Core_Eng",
        "Architect": "Core_Eng",
        "Lawyer": "Traditional", "Teacher": "Traditional"
    }

    # Iterate through all careers and replace their specific block
    for career, profile_key in career_mapping.items():
        prof = profiles[profile_key]
        
        # Regex to find the block for the specific career
        # We look for "Career Name": { ... "top_companies": [...] ... }
        # Since the format is strict in the file, we can do targeted string replacements within that block
        
        # Find the start index of the career block
        start_idx = content.find(f'"{career}": {{')
        if start_idx == -1:
            continue
            
        end_idx = content.find('    },', start_idx)
        if end_idx == -1:
            end_idx = content.find('    }', start_idx)
            
        block = content[start_idx:end_idx]
        
        # Replace values in the block
        new_block = re.sub(r'"demand": ".*?"', f'"demand": "{prof["demand"]}"', block)
        new_block = re.sub(r'"demand_color": ".*?"', f'"demand_color": "{prof["demand_color"]}"', new_block)
        new_block = re.sub(r'"salary_range": ".*?"', f'"salary_range": "{prof["salary"]}"', new_block)
        new_block = re.sub(r'"growth": ".*?"', f'"growth": "{prof["growth"]}"', new_block)
        new_block = re.sub(r'"top_companies": \[.*?\]', f'"top_companies": {prof["companies"]}', new_block)
        
        content = content[:start_idx] + new_block + content[end_idx:]

    with open('backend/ml/career_data.py', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Successfully updated career_data.py with realistic dynamic values!")

if __name__ == "__main__":
    update_career_data()
