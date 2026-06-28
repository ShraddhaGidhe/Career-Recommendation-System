-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Recommendations Table
CREATE TABLE IF NOT EXISTS recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    education_level VARCHAR(100) NOT NULL,
    specialization VARCHAR(100) NOT NULL,
    skills TEXT NOT NULL,
    interest VARCHAR(100) NOT NULL,
    certifications TEXT,
    cgpa FLOAT NOT NULL,
    predicted_career VARCHAR(100) NOT NULL,
    confidence FLOAT,
    top_matches JSON,
    explanation TEXT,
    career_info_json JSON,
    roadmap_json JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Roadmaps Table
CREATE TABLE IF NOT EXISTS user_roadmaps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    career_name VARCHAR(100) NOT NULL,
    skill_name VARCHAR(255) NOT NULL,
    status ENUM('Not Started', 'Learning', 'Completed') DEFAULT 'Not Started',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_career_skill (user_id, career_name, skill_name)
);