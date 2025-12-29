"""
Career Comparison Service
Allows users to compare careers across multiple dimensions
"""

import json
import os
from typing import List, Dict, Any, Optional

class CareerComparison:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.careers_data = self._load_careers_data()
        self.reality_data = self._load_reality_data()
        
    def _load_careers_data(self) -> Dict:
        """Load career data from JSON files"""
        careers = {}
        
        # Load global careers
        global_path = os.path.join(self.data_dir, 'careers.json')
        if os.path.exists(global_path):
            with open(global_path, 'r', encoding='utf-8') as f:
                global_careers = json.load(f)
                for career in global_careers:
                    careers[career['name']] = {**career, 'region': 'global'}
        
        # Load India careers
        india_path = os.path.join(self.data_dir, 'careers_india.json')
        if os.path.exists(india_path):
            with open(india_path, 'r', encoding='utf-8') as f:
                india_careers = json.load(f)
                for career in india_careers:
                    career_name = career['name']
                    if career_name in careers:
                        # Add India-specific data
                        careers[career_name]['india_salary'] = career.get('median_salary', 'N/A')
                        careers[career_name]['india_outlook'] = career.get('job_outlook', 'N/A')
                    else:
                        careers[career_name] = {**career, 'region': 'india'}
        
        return careers
    
    def _load_reality_data(self) -> Dict:
        """Load career reality check data"""
        reality_path = os.path.join(self.data_dir, 'career_reality_check.json')
        if os.path.exists(reality_path):
            with open(reality_path, 'r', encoding='utf-8') as f:
                return json.load(f).get('career_reality_data', {})
        return {}
    
    def get_available_careers(self, region: str = 'global') -> List[str]:
        """Get list of available careers for comparison"""
        if region == 'all':
            return list(self.careers_data.keys())
        
        careers = []
        for name, data in self.careers_data.items():
            if region == 'global' and (data.get('region') == 'global' or 'india_salary' in data):
                careers.append(name)
            elif region == 'india' and (data.get('region') == 'india' or 'india_salary' in data):
                careers.append(name)
        
        return sorted(careers)
    
    def _normalize_salary(self, salary_str: str) -> int:
        """Convert salary string to numeric value for comparison"""
        if not salary_str or salary_str == 'N/A':
            return 0
        
        # Remove currency symbols and commas
        clean_salary = salary_str.replace('$', '').replace('₹', '').replace(',', '').replace(' ', '')
        
        # Handle ranges (take average)
        if '-' in clean_salary:
            parts = clean_salary.split('-')
            try:
                low = float(parts[0])
                high = float(parts[1])
                return int((low + high) / 2)
            except:
                return 0
        
        # Handle single values
        try:
            # Convert lakhs to actual numbers for Indian salaries
            if 'lakh' in salary_str.lower() or 'l' in clean_salary.lower():
                clean_salary = clean_salary.lower().replace('lakh', '').replace('l', '')
                return int(float(clean_salary) * 100000)
            
            return int(float(clean_salary))
        except:
            return 0
    
    def _get_stress_level_score(self, stress_level: str) -> int:
        """Convert stress level to numeric score (1-5, higher = more stress)"""
        stress_mapping = {
            'low': 1,
            'medium-low': 2,
            'medium': 3,
            'medium-high': 4,
            'high': 5
        }
        return stress_mapping.get(stress_level.lower(), 3)
    
    def _get_work_life_balance_score(self, balance_desc: str) -> int:
        """Convert work-life balance description to score (1-5, higher = better balance)"""
        balance_desc = balance_desc.lower()
        
        if 'excellent' in balance_desc or 'great' in balance_desc:
            return 5
        elif 'good' in balance_desc or 'flexible' in balance_desc:
            return 4
        elif 'moderate' in balance_desc or 'balanced' in balance_desc:
            return 3
        elif 'challenging' in balance_desc or 'demanding' in balance_desc:
            return 2
        elif 'poor' in balance_desc or 'intense' in balance_desc:
            return 1
        else:
            return 3  # Default to moderate
    
    def compare_careers(self, career_names: List[str], region: str = 'global') -> Dict[str, Any]:
        """Compare multiple careers across key dimensions"""
        if len(career_names) < 2:
            return {"error": "Please select at least 2 careers to compare"}
        
        if len(career_names) > 5:
            return {"error": "Maximum 5 careers can be compared at once"}
        
        comparison_data = {
            "careers": [],
            "comparison_metrics": {
                "salary": {},
                "stress_level": {},
                "work_life_balance": {},
                "growth_rate": {},
                "skills_complexity": {}
            },
            "region": region
        }
        
        for career_name in career_names:
            if career_name not in self.careers_data:
                continue
                
            career_data = self.careers_data[career_name]
            reality_data = self.reality_data.get(career_name, {})
            
            # Get salary based on region
            if region == 'india' and 'india_salary' in career_data:
                salary = career_data['india_salary']
            else:
                salary = career_data.get('median_salary', 'N/A')
            
            # Get stress level and work-life balance from reality data
            reality_check = reality_data.get('reality_check', {})
            stress_level = reality_check.get('stress_level', 'Medium')
            work_life_balance = reality_check.get('work_life_balance', 'Moderate')
            
            # Calculate skills complexity (based on number of required skills)
            skills_count = len(career_data.get('required_skills', []))
            skills_complexity = min(5, max(1, skills_count // 2))  # Scale 1-5
            
            career_comparison = {
                "name": career_name,
                "salary": salary,
                "salary_numeric": self._normalize_salary(salary),
                "stress_level": stress_level,
                "stress_score": self._get_stress_level_score(stress_level),
                "work_life_balance": work_life_balance,
                "work_life_score": self._get_work_life_balance_score(work_life_balance),
                "growth_rate": career_data.get('growth_rate', 'N/A'),
                "growth_numeric": self._extract_growth_rate(career_data.get('growth_rate', '0%')),
                "required_skills": career_data.get('required_skills', []),
                "skills_complexity": skills_complexity,
                "description": career_data.get('description', ''),
                "job_outlook": career_data.get('job_outlook', 'N/A')
            }
            
            comparison_data["careers"].append(career_comparison)
        
        # Calculate rankings for each metric
        comparison_data["rankings"] = self._calculate_rankings(comparison_data["careers"])
        
        return comparison_data
    
    def _extract_growth_rate(self, growth_str: str) -> float:
        """Extract numeric growth rate from string"""
        if not growth_str or growth_str == 'N/A':
            return 0.0
        
        # Extract percentage
        import re
        match = re.search(r'(\d+(?:\.\d+)?)%?', growth_str)
        if match:
            return float(match.group(1))
        return 0.0
    
    def _calculate_rankings(self, careers: List[Dict]) -> Dict[str, List[str]]:
        """Calculate rankings for each metric"""
        rankings = {}
        
        # Salary ranking (higher is better)
        salary_sorted = sorted(careers, key=lambda x: x['salary_numeric'], reverse=True)
        rankings['salary'] = [career['name'] for career in salary_sorted]
        
        # Stress level ranking (lower stress is better)
        stress_sorted = sorted(careers, key=lambda x: x['stress_score'])
        rankings['stress_level'] = [career['name'] for career in stress_sorted]
        
        # Work-life balance ranking (higher score is better)
        balance_sorted = sorted(careers, key=lambda x: x['work_life_score'], reverse=True)
        rankings['work_life_balance'] = [career['name'] for career in balance_sorted]
        
        # Growth rate ranking (higher is better)
        growth_sorted = sorted(careers, key=lambda x: x['growth_numeric'], reverse=True)
        rankings['growth_rate'] = [career['name'] for career in growth_sorted]
        
        # Skills complexity ranking (lower complexity might be better for beginners)
        skills_sorted = sorted(careers, key=lambda x: x['skills_complexity'])
        rankings['skills_complexity'] = [career['name'] for career in skills_sorted]
        
        return rankings
    
    def get_detailed_comparison(self, career1: str, career2: str, region: str = 'global') -> Dict[str, Any]:
        """Get detailed side-by-side comparison of two careers"""
        comparison = self.compare_careers([career1, career2], region)
        
        if "error" in comparison:
            return comparison
        
        if len(comparison["careers"]) != 2:
            return {"error": "Both careers must be available for comparison"}
        
        career_a, career_b = comparison["careers"]
        
        detailed_comparison = {
            "career_a": career_a,
            "career_b": career_b,
            "winner_analysis": {
                "salary": career_a["name"] if career_a["salary_numeric"] > career_b["salary_numeric"] else career_b["name"],
                "work_life_balance": career_a["name"] if career_a["work_life_score"] > career_b["work_life_score"] else career_b["name"],
                "low_stress": career_a["name"] if career_a["stress_score"] < career_b["stress_score"] else career_b["name"],
                "growth_potential": career_a["name"] if career_a["growth_numeric"] > career_b["growth_numeric"] else career_b["name"],
                "easier_entry": career_a["name"] if career_a["skills_complexity"] < career_b["skills_complexity"] else career_b["name"]
            },
            "region": region
        }
        
        return detailed_comparison