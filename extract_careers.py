import json
import re

with open('backend/ml/career_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
careers = []
for line in lines:
    if line.startswith('    "') and '": {' in line:
        career = line.split('"')[1]
        careers.append(career)

with open('careers.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(careers))
