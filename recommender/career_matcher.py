import json
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class CareerMatcher:
    def __init__(self, region='global', mode='student'):
        self.region = region
        self.mode = mode
        self.mode_config = self._load_mode_config()
        self.careers_data = self._load_careers_data()
        self.skills_mapping = self._load_skills_mapping()
        
    def _load_mode_config(self):
        """Load mode and region configuration"""
        try:
            with open('data/mode_config.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_mode_config()
    
    def _load_careers_data(self):
        """Load career data based on region"""
        try:
            career_file = self.mode_config['regions'][self.region]['career_file']
            with open(f'data/{career_file}', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_careers()
    
    def _load_skills_mapping(self):
        """Load skills mapping data"""
        try:
            with open('data/skills_mapping.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_skills_mapping()
    
    def _get_default_mode_config(self):
        """Default mode configuration"""
        return {
            "regions": {
                "global": {"career_file": "careers.json", "currency": "USD", "salary_prefix": "$"},
                "india": {"career_file": "careers_india.json", "currency": "INR", "salary_prefix": "₹"}
            },
            "modes": {
                "student": {
                    "assessment_weight": {"interests": 0.45, "subjects": 0.25, "skills": 0.20, "personality": 0.10}
                },
                "professional": {
                    "assessment_weight": {"skills": 0.40, "interests": 0.30, "personality": 0.20, "subjects": 0.10}
                }
            }
        }
    
    def _get_default_careers(self):
        """Default career data if file doesn't exist"""
        return [
            {
                "name": "Software Engineer",
                "required_skills": ["programming", "problem_solving", "logical_thinking", "mathematics"],
                "interests": ["technology", "computers", "innovation", "problem_solving"],
                "subjects": ["computer_science", "mathematics", "physics"],
                "personality_traits": ["analytical", "detail_oriented", "creative"],
                "description": "Design and develop software applications and systems",
                "growth_rate": "22%",
                "median_salary": "$110,000"
            }
        ]
    
    def _get_default_skills_mapping(self):
        """Default skills mapping"""
        return {
            "subjects_to_skills": {
                "mathematics": ["logical_thinking", "problem_solving", "analysis"],
                "computer_science": ["programming", "logical_thinking", "problem_solving"],
                "psychology": ["empathy", "research", "communication"],
                "art": ["creativity", "design", "visual_thinking"],
                "business": ["strategy", "communication", "leadership"]
            }
        }
    
    def get_recommendations(self, interests, skills, subjects, personality, experience_level=None):
        """Get career recommendations based on user input, region, and mode"""
        user_profile = self._create_user_profile(interests, skills, subjects, personality, experience_level)
        career_scores = []
        
        for career in self.careers_data:
            score = self._calculate_match_score(user_profile, career)
            career_scores.append((career, score))
        
        # Sort by score and return top recommendations
        career_scores.sort(key=lambda x: x[1], reverse=True)
        return [career for career, score in career_scores[:5]]
    
    def _create_user_profile(self, interests, skills, subjects, personality, experience_level=None):
        """Create a user profile from inputs"""
        # Add skills derived from subjects
        derived_skills = []
        for subject in subjects:
            if subject in self.skills_mapping.get("subjects_to_skills", {}):
                derived_skills.extend(self.skills_mapping["subjects_to_skills"][subject])
        
        all_skills = list(set(skills + derived_skills))
        
        return {
            "interests": interests,
            "skills": all_skills,
            "subjects": subjects,
            "personality": personality,
            "experience_level": experience_level,
            "region": self.region,
            "mode": self.mode
        }
    
    def _calculate_match_score(self, user_profile, career):
        """Calculate how well a career matches the user profile with mode-specific weights"""
        # Get mode-specific weights
        weights = self.mode_config['modes'][self.mode]['assessment_weight']
        
        score = 0
        
        # Interest matching
        interest_match = len(set(user_profile["interests"]) & set(career["interests"]))
        interest_score = interest_match / max(len(career["interests"]), 1)
        score += interest_score * weights['interests']
        
        # Skills matching
        skill_match = len(set(user_profile["skills"]) & set(career["required_skills"]))
        skill_score = skill_match / max(len(career["required_skills"]), 1)
        score += skill_score * weights['skills']
        
        # Subject matching
        subject_match = len(set(user_profile["subjects"]) & set(career["subjects"]))
        subject_score = subject_match / max(len(career["subjects"]), 1) if career["subjects"] else 0
        score += subject_score * weights['subjects']
        
        # Personality matching
        personality_traits = user_profile["personality"].get("traits", [])
        personality_match = len(set(personality_traits) & set(career["personality_traits"]))
        personality_score = personality_match / max(len(career["personality_traits"]), 1)
        score += personality_score * weights['personality']
        
        # Experience level adjustment for professional mode
        if self.mode == 'professional' and user_profile.get('experience_level'):
            score = self._adjust_for_experience(score, user_profile['experience_level'], career)
        
        return score
    
    def _adjust_for_experience(self, base_score, experience_level, career):
        """Adjust score based on experience level for professional mode"""
        # Add logic to boost scores for careers that match experience level
        # For now, return base score
        return base_score
    
    def get_visualization_data(self, user_data):
        """Generate data for career graph visualization"""
        recommendations = self.get_recommendations(
            user_data.get('interests', []),
            user_data.get('skills', []),
            user_data.get('subjects', []),
            user_data.get('personality', {}),
            user_data.get('experience_level')
        )
        
        viz_data = {
            "nodes": [],
            "links": []
        }
        
        # Add user node
        viz_data["nodes"].append({
            "id": "user",
            "name": f"You ({self.mode.title()})",
            "type": "user",
            "size": 20,
            "region": self.region
        })
        
        # Add career nodes
        for i, career in enumerate(recommendations[:3]):  # Top 3 for visualization
            viz_data["nodes"].append({
                "id": f"career_{i}",
                "name": career["name"],
                "type": "career",
                "size": 15,
                "salary": career["median_salary"],
                "growth": career["growth_rate"],
                "region": self.region
            })
            
            # Add link from user to career
            viz_data["links"].append({
                "source": "user",
                "target": f"career_{i}",
                "strength": self._calculate_match_score(
                    self._create_user_profile(
                        user_data.get('interests', []),
                        user_data.get('skills', []),
                        user_data.get('subjects', []),
                        user_data.get('personality', {}),
                        user_data.get('experience_level')
                    ),
                    career
                )
            })
        
        return viz_data
    
    def get_region_info(self):
        """Get information about the current region"""
        return self.mode_config['regions'].get(self.region, {})
    
    def get_mode_info(self):
        """Get information about the current mode"""
        return self.mode_config['modes'].get(self.mode, {})