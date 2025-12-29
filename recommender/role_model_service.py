import json
import random
from datetime import datetime, timedelta

class RoleModelService:
    def __init__(self, region='global'):
        self.region = region
        self.role_models = self._load_role_models()
        self.career_tips = self._load_career_tips()
    
    def _load_role_models(self):
        """Load role models data from JSON file based on region"""
        try:
            if self.region == 'india':
                with open('data/role_models_india.json', 'r') as f:
                    return json.load(f)
            else:
                with open('data/role_models.json', 'r') as f:
                    return json.load(f)
        except FileNotFoundError:
            return []
    
    def _load_career_tips(self):
        """Load career tips data from JSON file"""
        try:
            with open('data/career_tips.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def get_role_models_for_career(self, career_name):
        """Get role models for a specific career"""
        matching_models = []
        for model in self.role_models:
            if model['career'].lower() in career_name.lower() or career_name.lower() in model['career'].lower():
                matching_models.append(model)
        
        # If no exact match, return all models (student can learn from any field)
        if not matching_models:
            matching_models = self.role_models
        
        return matching_models
    
    def get_role_models_for_careers(self, career_list):
        """Get role models for multiple careers"""
        all_models = []
        seen_names = set()
        
        for career in career_list:
            models = self.get_role_models_for_career(career['name'])
            for model in models:
                if model['name'] not in seen_names:
                    all_models.append(model)
                    seen_names.add(model['name'])
        
        return all_models[:3]  # Return top 3 to avoid overwhelming
    
    def get_daily_tip(self, career_focus=None, user_id=None, mode='student'):
        """Get daily career tip, optionally filtered by career focus and mode"""
        # Filter tips by career focus if provided
        relevant_tips = self.career_tips
        if career_focus:
            relevant_tips = [
                tip for tip in self.career_tips 
                if career_focus in tip['career_focus'] or 'All careers' in tip['career_focus']
            ]
        
        # Filter by mode-specific categories
        if mode == 'professional':
            professional_categories = ['career_advancement', 'leadership', 'industry_transition', 'networking']
            relevant_tips = [tip for tip in relevant_tips if tip['category'] in professional_categories]
        
        # Use user_id and date to ensure same tip per day per user
        if user_id:
            # Create a seed based on user_id and current date
            today = datetime.now().strftime('%Y-%m-%d')
            seed = hash(f"{user_id}_{today}") % len(relevant_tips)
            return relevant_tips[seed]
        else:
            # Random tip for anonymous users
            return random.choice(relevant_tips) if relevant_tips else self.career_tips[0]
    
    def get_weekly_tips(self, career_focus=None, mode='student'):
        """Get a week's worth of career tips"""
        relevant_tips = self.career_tips
        if career_focus:
            relevant_tips = [
                tip for tip in self.career_tips 
                if career_focus in tip['career_focus'] or 'All careers' in tip['career_focus']
            ]
        
        # Filter by mode
        if mode == 'professional':
            professional_categories = ['career_advancement', 'leadership', 'industry_transition', 'networking']
            relevant_tips = [tip for tip in relevant_tips if tip['category'] in professional_categories]
        
        # Return 7 random tips for the week
        return random.sample(relevant_tips, min(7, len(relevant_tips)))
    
    def get_tip_by_category(self, category):
        """Get tips by specific category"""
        return [tip for tip in self.career_tips if tip['category'] == category]
    
    def get_inspiration_quote(self, career_name=None):
        """Get an inspirational quote from role models"""
        if career_name:
            models = self.get_role_models_for_career(career_name)
        else:
            models = self.role_models
        
        if models:
            model = random.choice(models)
            return {
                'quote': model['inspiration_quote'],
                'author': model['name'],
                'title': model['title']
            }
        return None
    
    def get_career_path_example(self, career_name):
        """Get career path examples from role models"""
        models = self.get_role_models_for_career(career_name)
        if models:
            model = random.choice(models)
            return {
                'name': model['name'],
                'career_path': model['career_path'],
                'advice': model['advice'],
                'achievements': model['achievements']
            }
        return None
    
    def search_role_models(self, query):
        """Search role models by name, career, or skills"""
        query = query.lower()
        results = []
        
        for model in self.role_models:
            # Search in name, career, title, and skills
            searchable_text = f"{model['name']} {model['career']} {model['title']} {' '.join(model['key_skills'])}".lower()
            if query in searchable_text:
                results.append(model)
        
        return results
    
    def get_skill_development_tips(self, skills_to_develop):
        """Get specific tips for developing certain skills"""
        skill_tips = []
        
        for skill in skills_to_develop:
            # Find tips that might help develop this skill
            for tip in self.career_tips:
                if skill.lower() in tip['tip'].lower() or skill.lower() in tip['title'].lower():
                    skill_tips.append({
                        'skill': skill,
                        'tip': tip
                    })
        
        return skill_tips[:5]  # Return top 5 relevant tips
    
    def get_region_specific_advice(self, career_name):
        """Get region-specific career advice"""
        models = self.get_role_models_for_career(career_name)
        region_advice = []
        
        for model in models:
            if 'indian_context' in model:
                region_advice.append({
                    'name': model['name'],
                    'context': model['indian_context'],
                    'advice': model['advice']
                })
        
        return region_advice