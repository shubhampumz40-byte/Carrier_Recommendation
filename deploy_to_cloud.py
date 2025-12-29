#!/usr/bin/env python3
"""
Career Compass - Cloud Deployment Helper
This script helps you prepare and deploy your Career Compass to the cloud
"""

import os
import subprocess
import sys
import json
from datetime import datetime

class CloudDeployer:
    def __init__(self):
        self.project_name = "career-compass"
        self.current_dir = os.getcwd()
        
    def log(self, message):
        """Log messages with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def check_requirements(self):
        """Check if all required files exist"""
        required_files = [
            'requirements.txt',
            'run.py',
            'app/__init__.py',
            'Procfile',
            'railway.json'
        ]
        
        missing_files = []
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
                
        if missing_files:
            self.log(f"❌ Missing files: {', '.join(missing_files)}")
            return False
        else:
            self.log("✅ All required files present")
            return True
            
    def create_gitignore(self):
        """Create .gitignore file"""
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Local files
*.log
.env
.env.local

# Executables
*.exe
ngrok.exe
cloudflared.exe
ngrok.zip

# Test files
test_*.py
"""
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        self.log("✅ Created .gitignore file")
        
    def show_deployment_options(self):
        """Show available deployment options"""
        print("\n🚀 Cloud Deployment Options:")
        print("=" * 50)
        
        options = [
            {
                "name": "Railway",
                "url": "https://railway.app",
                "pros": ["$5/month free credit", "Easy GitHub integration", "Auto-deploy"],
                "steps": [
                    "1. Create GitHub repository",
                    "2. Upload your code to GitHub",
                    "3. Connect Railway to GitHub",
                    "4. Deploy automatically!"
                ]
            },
            {
                "name": "Render",
                "url": "https://render.com",
                "pros": ["750 hours/month free", "Custom domains", "SSL included"],
                "steps": [
                    "1. Create GitHub repository",
                    "2. Upload your code to GitHub", 
                    "3. Connect Render to GitHub",
                    "4. Configure build settings"
                ]
            },
            {
                "name": "Heroku",
                "url": "https://heroku.com",
                "pros": ["Industry standard", "Reliable", "Good documentation"],
                "steps": [
                    "1. Install Heroku CLI",
                    "2. Create Heroku app",
                    "3. Push code with Git",
                    "4. App goes live!"
                ]
            }
        ]
        
        for i, option in enumerate(options, 1):
            print(f"\n{i}. {option['name']} ⭐")
            print(f"   URL: {option['url']}")
            print(f"   Pros: {', '.join(option['pros'])}")
            print("   Steps:")
            for step in option['steps']:
                print(f"     {step}")
                
    def create_readme(self):
        """Create README for GitHub"""
        readme_content = f"""# 🧭 Career Compass - AI Career Recommender

An intelligent career recommendation system that provides personalized, explainable career suggestions for students based on their interests, skills, subjects, and personality.

## ✨ Features

- **Personalized Recommendations**: AI-powered career matching
- **36 Role Models**: Inspiring professionals from Steve Jobs to Ratan Tata
- **Trending Careers**: 2025-2035 career opportunities radar
- **Career Simulation**: "Day in the life" experiences
- **Skills Gap Analysis**: Personalized learning paths
- **Reality Check**: Honest career insights and challenges
- **Daily Tips**: Actionable career advice

## 🚀 Live Demo

Visit: [Career Compass Live](https://your-app-url.com)

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Data**: JSON-based career database
- **AI**: Custom recommendation algorithms
- **Deployment**: Cloud-ready (Railway/Render/Heroku)

## 📊 Career Database

- **12 Updated Careers** with 2025 salary data
- **Global & India** specific career paths
- **Student & Professional** modes
- **Latest market data** from official sources

## 🎯 Getting Started

### Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/career-compass.git
cd career-compass

# Install dependencies
pip install -r requirements.txt

# Run application
python run.py
```

### Cloud Deployment
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 📱 Share

Perfect for:
- Students exploring career options
- Career counselors and educators
- Parents guiding their children
- Professionals considering career changes

## 🤝 Contributing

Contributions welcome! Please read our contributing guidelines.

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with ❤️ for students exploring their career paths in 2025 and beyond**

*Last Updated: {datetime.now().strftime('%B %Y')}*
"""
        
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        self.log("✅ Created README.md file")
        
    def prepare_for_deployment(self):
        """Prepare all files for cloud deployment"""
        self.log("🚀 Preparing Career Compass for cloud deployment...")
        
        # Check requirements
        if not self.check_requirements():
            self.log("❌ Please ensure all required files are present")
            return False
            
        # Create additional files
        self.create_gitignore()
        self.create_readme()
        
        self.log("✅ All files prepared for deployment!")
        return True
        
    def show_next_steps(self):
        """Show next steps for deployment"""
        print("\n🎯 Next Steps:")
        print("=" * 30)
        print("1. Create GitHub repository at: https://github.com/new")
        print("2. Upload all your project files to GitHub")
        print("3. Choose a cloud platform (Railway recommended)")
        print("4. Connect your GitHub repo to the platform")
        print("5. Your Career Compass will be live 24/7!")
        print("\n📖 See DEPLOYMENT_GUIDE.md for detailed instructions")
        
    def run(self):
        """Main deployment preparation"""
        print("🧭 Career Compass - Cloud Deployment Helper")
        print("=" * 50)
        
        if self.prepare_for_deployment():
            self.show_deployment_options()
            self.show_next_steps()
            
            print("\n🎉 Your Career Compass is ready for 24/7 cloud hosting!")
            print("Choose your preferred platform and follow the deployment guide.")
        else:
            print("\n❌ Deployment preparation failed. Please check the errors above.")

if __name__ == "__main__":
    deployer = CloudDeployer()
    deployer.run()