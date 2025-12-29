"""
Skills Gap Analyzer - Analyzes the gap between user's current skills and career requirements
"""

import json
from typing import Dict, List, Tuple, Any

class SkillsGapAnalyzer:
    def __init__(self):
        self.skills_data = self._load_skills_data()
        self.learning_resources = self._load_learning_resources()
    
    def _load_skills_data(self):
        """Load comprehensive skills data"""
        try:
            with open('data/skills_mapping.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_skills_data()
    
    def _load_learning_resources(self):
        """Load learning resources for skill development"""
        return {
            "programming": {
                "beginner": ["Codecademy Python", "freeCodeCamp", "Python.org Tutorial"],
                "intermediate": ["LeetCode", "HackerRank", "Real Python"],
                "advanced": ["System Design Interview", "Clean Code Book", "Design Patterns"],
                "time_estimate": "3-6 months"
            },
            "machine_learning": {
                "beginner": ["Andrew Ng Coursera", "Kaggle Learn", "Scikit-learn Tutorial"],
                "intermediate": ["Fast.ai", "Deep Learning Specialization", "Hands-On ML Book"],
                "advanced": ["Papers with Code", "Google AI Research", "Advanced ML Courses"],
                "time_estimate": "6-12 months"
            },
            "data_analysis": {
                "beginner": ["Excel Basics", "SQL Tutorial", "Tableau Public"],
                "intermediate": ["Python Pandas", "R Programming", "Power BI"],
                "advanced": ["Advanced Statistics", "A/B Testing", "Data Science Bootcamp"],
                "time_estimate": "2-4 months"
            },
            "leadership": {
                "beginner": ["Leadership Books", "Team Management Basics", "Communication Skills"],
                "intermediate": ["MBA Leadership Courses", "Conflict Resolution", "Strategic Thinking"],
                "advanced": ["Executive Leadership Programs", "Change Management", "Organizational Psychology"],
                "time_estimate": "1-2 years"
            },
            "design": {
                "beginner": ["Figma Basics", "Design Principles", "Color Theory"],
                "intermediate": ["UX Design Course", "Prototyping", "User Research"],
                "advanced": ["Design Systems", "Advanced Prototyping", "Design Leadership"],
                "time_estimate": "3-6 months"
            },
            "cybersecurity": {
                "beginner": ["CompTIA Security+", "Cybersecurity Basics", "Network Fundamentals"],
                "intermediate": ["Ethical Hacking", "CISSP Prep", "Incident Response"],
                "advanced": ["Advanced Penetration Testing", "Security Architecture", "Threat Intelligence"],
                "time_estimate": "6-12 months"
            },
            "communication": {
                "beginner": ["Public Speaking Basics", "Writing Skills", "Active Listening"],
                "intermediate": ["Presentation Skills", "Technical Writing", "Cross-cultural Communication"],
                "advanced": ["Executive Communication", "Negotiation Skills", "Crisis Communication"],
                "time_estimate": "2-6 months"
            },
            "project_management": {
                "beginner": ["Project Management Basics", "Agile Fundamentals", "Time Management"],
                "intermediate": ["PMP Certification", "Scrum Master", "Risk Management"],
                "advanced": ["Program Management", "Portfolio Management", "Organizational Change"],
                "time_estimate": "3-6 months"
            }
        }
    
    def _get_default_skills_data(self):
        """Default skills mapping if file doesn't exist"""
        return {
            "subjects_to_skills": {
                "computer_science": ["programming", "algorithms", "data_structures", "system_design"],
                "mathematics": ["analytical_thinking", "problem_solving", "statistics", "logical_reasoning"],
                "business": ["strategic_thinking", "communication", "leadership", "project_management"],
                "psychology": ["empathy", "research", "communication", "analytical_thinking"],
                "art": ["creativity", "design", "visual_thinking", "attention_to_detail"]
            },
            "skill_categories": {
                "technical": ["programming", "machine_learning", "data_analysis", "cybersecurity", "design"],
                "soft": ["communication", "leadership", "teamwork", "problem_solving", "creativity"],
                "business": ["project_management", "strategic_thinking", "marketing", "sales", "finance"]
            }
        }
    
    def analyze_skills_gap(self, user_skills: List[str], career_requirements: Dict[str, Any], 
                          user_subjects: List[str] = None, user_interests: List[str] = None) -> Dict[str, Any]:
        """
        Analyze the gap between user's current skills and career requirements
        
        Args:
            user_skills: List of user's current skills
            career_requirements: Career data including required_skills
            user_subjects: User's academic subjects (optional)
            user_interests: User's interests (optional)
        
        Returns:
            Dictionary with gap analysis results
        """
        # Normalize skills to lowercase for comparison
        user_skills_normalized = [skill.lower().replace(' ', '_') for skill in user_skills]
        required_skills = [skill.lower().replace(' ', '_') for skill in career_requirements.get('required_skills', [])]
        
        # Add derived skills from subjects
        if user_subjects:
            derived_skills = self._derive_skills_from_subjects(user_subjects)
            user_skills_normalized.extend(derived_skills)
        
        # Remove duplicates
        user_skills_normalized = list(set(user_skills_normalized))
        
        # Calculate gaps
        current_skills = [skill for skill in required_skills if skill in user_skills_normalized]
        missing_skills = [skill for skill in required_skills if skill not in user_skills_normalized]
        
        # Calculate skill match percentage
        skill_match_percentage = (len(current_skills) / len(required_skills) * 100) if required_skills else 100
        
        # Categorize skills
        skill_categories = self._categorize_skills(current_skills, missing_skills)
        
        # Generate learning path
        learning_path = self._generate_learning_path(missing_skills)
        
        # Estimate time to bridge gap
        time_estimate = self._estimate_learning_time(missing_skills)
        
        # Get skill priorities
        skill_priorities = self._prioritize_missing_skills(missing_skills, career_requirements)
        
        return {
            "career_name": career_requirements.get('name', 'Unknown'),
            "skill_match_percentage": round(skill_match_percentage, 1),
            "current_skills": {
                "count": len(current_skills),
                "skills": current_skills,
                "categories": skill_categories["current"]
            },
            "missing_skills": {
                "count": len(missing_skills),
                "skills": missing_skills,
                "categories": skill_categories["missing"],
                "priorities": skill_priorities
            },
            "learning_path": learning_path,
            "time_estimate": time_estimate,
            "readiness_level": self._assess_readiness_level(skill_match_percentage),
            "next_steps": self._generate_next_steps(missing_skills, skill_match_percentage),
            "skill_development_plan": self._create_development_plan(missing_skills)
        }
    
    def _derive_skills_from_subjects(self, subjects: List[str]) -> List[str]:
        """Derive skills from academic subjects"""
        derived_skills = []
        subjects_to_skills = self.skills_data.get("subjects_to_skills", {})
        
        for subject in subjects:
            subject_normalized = subject.lower().replace(' ', '_')
            if subject_normalized in subjects_to_skills:
                derived_skills.extend(subjects_to_skills[subject_normalized])
        
        return derived_skills
    
    def _categorize_skills(self, current_skills: List[str], missing_skills: List[str]) -> Dict[str, Dict[str, List[str]]]:
        """Categorize skills into technical, soft, and business skills"""
        skill_categories = self.skills_data.get("skill_categories", {
            "technical": ["programming", "machine_learning", "data_analysis"],
            "soft": ["communication", "leadership", "teamwork"],
            "business": ["project_management", "strategic_thinking", "marketing"]
        })
        
        def categorize_skill_list(skills):
            categorized = {"technical": [], "soft": [], "business": [], "other": []}
            for skill in skills:
                categorized_flag = False
                for category, category_skills in skill_categories.items():
                    if any(cat_skill in skill for cat_skill in category_skills):
                        categorized[category].append(skill)
                        categorized_flag = True
                        break
                if not categorized_flag:
                    categorized["other"].append(skill)
            return categorized
        
        return {
            "current": categorize_skill_list(current_skills),
            "missing": categorize_skill_list(missing_skills)
        }
    
    def _prioritize_missing_skills(self, missing_skills: List[str], career_requirements: Dict[str, Any]) -> Dict[str, List[str]]:
        """Prioritize missing skills based on importance"""
        # Simple prioritization based on skill type and career level
        high_priority = []
        medium_priority = []
        low_priority = []
        
        critical_skills = ["programming", "machine_learning", "data_analysis", "leadership", "communication"]
        
        for skill in missing_skills:
            if any(critical in skill for critical in critical_skills):
                high_priority.append(skill)
            elif "management" in skill or "strategy" in skill:
                medium_priority.append(skill)
            else:
                low_priority.append(skill)
        
        return {
            "high": high_priority,
            "medium": medium_priority,
            "low": low_priority
        }
    
    def _generate_learning_path(self, missing_skills: List[str]) -> List[Dict[str, Any]]:
        """Generate a learning path for missing skills"""
        learning_path = []
        
        for skill in missing_skills:
            # Find matching learning resources
            matching_resource = None
            for resource_key, resource_data in self.learning_resources.items():
                if resource_key in skill or any(word in skill for word in resource_key.split('_')):
                    matching_resource = resource_data
                    break
            
            if matching_resource:
                learning_path.append({
                    "skill": skill,
                    "resources": matching_resource,
                    "difficulty": "beginner"  # Default to beginner
                })
            else:
                # Generic learning path
                learning_path.append({
                    "skill": skill,
                    "resources": {
                        "beginner": [f"Online courses for {skill}", f"{skill} tutorials", f"Books on {skill}"],
                        "time_estimate": "2-4 months"
                    },
                    "difficulty": "beginner"
                })
        
        return learning_path
    
    def _estimate_learning_time(self, missing_skills: List[str]) -> Dict[str, str]:
        """Estimate time needed to learn missing skills"""
        if not missing_skills:
            return {"total": "0 months", "breakdown": "No skills to learn"}
        
        total_months = 0
        breakdown = []
        
        for skill in missing_skills:
            # Estimate based on skill complexity
            if any(complex_skill in skill for complex_skill in ["machine_learning", "programming", "leadership"]):
                months = 6
            elif any(medium_skill in skill for medium_skill in ["data_analysis", "design", "project_management"]):
                months = 3
            else:
                months = 2
            
            total_months += months
            breakdown.append(f"{skill}: {months} months")
        
        # Adjust for parallel learning
        adjusted_total = max(total_months // 2, 3)  # Assume some parallel learning
        
        return {
            "total": f"{adjusted_total} months",
            "breakdown": breakdown,
            "note": "Estimates assume part-time learning with some skills learned in parallel"
        }
    
    def _assess_readiness_level(self, skill_match_percentage: float) -> Dict[str, Any]:
        """Assess user's readiness level for the career"""
        if skill_match_percentage >= 80:
            level = "Ready"
            color = "success"
            description = "You have most required skills and can start applying"
        elif skill_match_percentage >= 60:
            level = "Nearly Ready"
            color = "warning"
            description = "You have good foundation, need to develop a few key skills"
        elif skill_match_percentage >= 40:
            level = "Developing"
            color = "info"
            description = "You have some relevant skills, significant development needed"
        else:
            level = "Early Stage"
            color = "danger"
            description = "Substantial skill development required before pursuing this career"
        
        return {
            "level": level,
            "color": color,
            "description": description,
            "percentage": skill_match_percentage
        }
    
    def _generate_next_steps(self, missing_skills: List[str], skill_match_percentage: float) -> List[str]:
        """Generate actionable next steps"""
        next_steps = []
        
        if skill_match_percentage >= 80:
            next_steps = [
                "Start applying for entry-level positions",
                "Build a portfolio showcasing your skills",
                "Network with professionals in the field",
                "Consider internships or freelance projects"
            ]
        elif skill_match_percentage >= 60:
            next_steps = [
                "Focus on developing 2-3 key missing skills",
                "Take online courses or bootcamps",
                "Build projects to demonstrate new skills",
                "Seek mentorship from industry professionals"
            ]
        elif missing_skills:
            # Prioritize top 3 missing skills
            priority_skills = missing_skills[:3]
            next_steps = [
                f"Start learning {priority_skills[0]} immediately",
                "Dedicate 10-15 hours per week to skill development",
                "Join online communities and forums",
                "Consider formal education or certification programs"
            ]
            
            if len(priority_skills) > 1:
                next_steps.append(f"Plan to learn {priority_skills[1]} after mastering the first skill")
        
        return next_steps
    
    def _create_development_plan(self, missing_skills: List[str]) -> Dict[str, Any]:
        """Create a structured 6-month development plan"""
        if not missing_skills:
            return {"message": "No skill development needed - you're ready!"}
        
        # Divide skills into phases
        high_priority = missing_skills[:2]  # First 2 skills
        medium_priority = missing_skills[2:4]  # Next 2 skills
        low_priority = missing_skills[4:]  # Remaining skills
        
        plan = {
            "phase_1": {
                "duration": "Months 1-2",
                "focus": "Foundation Building",
                "skills": high_priority,
                "activities": [
                    "Complete beginner courses",
                    "Practice daily (1-2 hours)",
                    "Join learning communities"
                ]
            },
            "phase_2": {
                "duration": "Months 3-4", 
                "focus": "Skill Application",
                "skills": medium_priority,
                "activities": [
                    "Work on practical projects",
                    "Seek feedback from experts",
                    "Build portfolio pieces"
                ]
            },
            "phase_3": {
                "duration": "Months 5-6",
                "focus": "Advanced Development",
                "skills": low_priority,
                "activities": [
                    "Take advanced courses",
                    "Contribute to open source",
                    "Network with professionals"
                ]
            }
        }
        
        return plan