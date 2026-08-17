from pathlib import Path
p=Path('README.md')
s=p.read_text(encoding='utf-8')
s=s.replace('<p align="center">\n  <img src="https://skillicons.dev/icons?i=python,django,react,ts,postgres,docker,nginx,github" alt="Stack tecnológico de EcoHome" />\n</p>\n\n','')
s=s.replace('### Backend\n\n','### ⚙️ Backend\n\n<p>\n  <img src="https://skillicons.dev/icons?i=python,django" alt="Python y Django" />\n</p>\n\n')
s=s.replace('### Frontend\n\n','### 🎨 Frontend\n\n<p>\n  <img src="https://skillicons.dev/icons?i=react,ts,vite" alt="React, TypeScript y Vite" />\n</p>\n\n')
s=s.replace('### Datos e IoT\n\n','### 🗄️ Datos e IoT\n\n<p>\n  <img src="https://skillicons.dev/icons?i=postgres" alt="PostgreSQL" />\n  <img src="https://img.shields.io/badge/MQTT-Eclipse%20Mosquitto-660066?style=flat-square&logo=eclipsemosquitto&logoColor=white" alt="MQTT y Eclipse Mosquitto" />\n</p>\n\n')
s=s.replace('### DevOps\n\n','### 🧰 DevOps\n\n<p>\n  <img src="https://skillicons.dev/icons?i=docker,nginx,github,githubactions" alt="Docker, Nginx, GitHub y GitHub Actions" />\n</p>\n\n')
p.write_text(s,encoding='utf-8')
