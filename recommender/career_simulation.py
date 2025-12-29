"""
Career Simulation Service
Provides "A day in the life" simulations for different careers
"""

import json
import os
from typing import Dict, List, Any, Optional

class CareerSimulation:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.simulations_data = self._load_simulations_data()
        
    def _load_simulations_data(self) -> Dict:
        """Load career simulation data from JSON file"""
        simulations_path = os.path.join(self.data_dir, 'career_simulations.json')
        if os.path.exists(simulations_path):
            with open(simulations_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def get_available_careers(self) -> List[str]:
        """Get list of careers available for simulation"""
        return list(self.simulations_data.get('career_simulations', {}).keys())
    
    def get_career_simulation(self, career_name: str, region: str = 'global') -> Dict[str, Any]:
        """Get complete simulation data for a specific career"""
        simulations = self.simulations_data.get('career_simulations', {})
        
        if career_name not in simulations:
            return {"error": f"Simulation not available for {career_name}"}
        
        simulation = simulations[career_name].copy()
        
        # Add region-specific information if available
        if 'region_specific' in simulation and region in simulation['region_specific']:
            region_data = simulation['region_specific'][region]
            simulation['salary_range'] = region_data.get('salary', simulation['salary_range'])
            simulation['work_culture'] = region_data.get('work_culture', 'Standard work culture')
        
        # Calculate additional metrics
        simulation['total_tasks'] = len(simulation['daily_schedule'])
        simulation['peak_stress_time'] = self._find_peak_stress_time(simulation['daily_schedule'])
        simulation['stress_distribution'] = self._calculate_stress_distribution(simulation['daily_schedule'])
        simulation['work_intensity'] = self._calculate_work_intensity(simulation['daily_schedule'])
        
        return simulation
    
    def _find_peak_stress_time(self, schedule: List[Dict]) -> Dict[str, Any]:
        """Find the time period with highest stress level"""
        max_stress = 0
        peak_time = None
        peak_task = None
        
        for task in schedule:
            if task['stress_level'] > max_stress:
                max_stress = task['stress_level']
                peak_time = task['time']
                peak_task = task['task']
        
        return {
            'time': peak_time,
            'task': peak_task,
            'stress_level': max_stress
        }
    
    def _calculate_stress_distribution(self, schedule: List[Dict]) -> Dict[str, int]:
        """Calculate distribution of stress levels throughout the day"""
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for task in schedule:
            stress_level = task['stress_level']
            distribution[stress_level] += 1
        
        return distribution
    
    def _calculate_work_intensity(self, schedule: List[Dict]) -> Dict[str, Any]:
        """Calculate work intensity metrics"""
        total_duration = sum(task['duration'] for task in schedule)
        total_stress_weighted_time = sum(task['duration'] * task['stress_level'] for task in schedule)
        
        avg_intensity = total_stress_weighted_time / total_duration if total_duration > 0 else 0
        
        # Find longest continuous work period
        max_continuous_work = 0
        current_continuous = 0
        
        for task in schedule:
            if task['stress_level'] >= 2:  # Consider stress level 2+ as active work
                current_continuous += task['duration']
                max_continuous_work = max(max_continuous_work, current_continuous)
            else:
                current_continuous = 0
        
        return {
            'total_work_minutes': total_duration,
            'average_intensity': round(avg_intensity, 2),
            'max_continuous_work_minutes': max_continuous_work,
            'work_life_balance_score': self._calculate_work_life_balance_score(schedule)
        }
    
    def _calculate_work_life_balance_score(self, schedule: List[Dict]) -> int:
        """Calculate work-life balance score (1-5, higher is better)"""
        high_stress_tasks = sum(1 for task in schedule if task['stress_level'] >= 4)
        total_tasks = len(schedule)
        break_tasks = sum(1 for task in schedule if task['stress_level'] <= 1)
        
        # Simple scoring algorithm
        if high_stress_tasks / total_tasks > 0.4:
            return 2  # Poor balance
        elif high_stress_tasks / total_tasks > 0.2:
            return 3  # Moderate balance
        elif break_tasks / total_tasks > 0.2:
            return 4  # Good balance
        else:
            return 3  # Average balance
    
    def get_simulation_summary(self, career_name: str, region: str = 'global') -> Dict[str, Any]:
        """Get a condensed summary of the career simulation"""
        simulation = self.get_career_simulation(career_name, region)
        
        if "error" in simulation:
            return simulation
        
        return {
            'career_title': simulation['career_title'],
            'overview': simulation['overview'],
            'working_hours': simulation['working_hours'],
            'average_stress_level': simulation['average_stress_level'],
            'work_life_balance': simulation['work_life_balance'],
            'salary_range': simulation['salary_range'],
            'key_stress_factors': simulation['stress_factors'][:3],  # Top 3
            'key_rewards': simulation['rewards'][:3],  # Top 3
            'peak_stress_time': simulation['peak_stress_time'],
            'work_intensity': simulation['work_intensity']
        }
    
    def compare_simulations(self, career_names: List[str], region: str = 'global') -> Dict[str, Any]:
        """Compare multiple career simulations"""
        if len(career_names) < 2:
            return {"error": "Please select at least 2 careers to compare"}
        
        comparisons = []
        
        for career_name in career_names:
            summary = self.get_simulation_summary(career_name, region)
            if "error" not in summary:
                comparisons.append(summary)
        
        if len(comparisons) < 2:
            return {"error": "Not enough valid careers for comparison"}
        
        # Calculate comparison metrics
        comparison_result = {
            'careers': comparisons,
            'rankings': {
                'lowest_stress': sorted(comparisons, key=lambda x: x['average_stress_level']),
                'best_work_life_balance': sorted(comparisons, key=lambda x: x['work_intensity']['work_life_balance_score'], reverse=True),
                'shortest_hours': sorted(comparisons, key=lambda x: x['working_hours']['total_hours']),
                'highest_intensity': sorted(comparisons, key=lambda x: x['work_intensity']['average_intensity'], reverse=True)
            }
        }
        
        return comparison_result
    
    def get_stress_timeline(self, career_name: str, region: str = 'global') -> Dict[str, Any]:
        """Get stress level timeline throughout the day"""
        simulation = self.get_career_simulation(career_name, region)
        
        if "error" in simulation:
            return simulation
        
        timeline = []
        for task in simulation['daily_schedule']:
            timeline.append({
                'time': task['time'],
                'task': task['task'],
                'stress_level': task['stress_level'],
                'duration': task['duration'],
                'description': task['description']
            })
        
        return {
            'career_title': simulation['career_title'],
            'timeline': timeline,
            'stress_scale': self.simulations_data.get('simulation_metadata', {}).get('stress_scale', {}),
            'average_stress': simulation['average_stress_level']
        }
    
    def get_career_insights(self, career_name: str, region: str = 'global') -> Dict[str, Any]:
        """Get detailed insights and analysis for a career"""
        simulation = self.get_career_simulation(career_name, region)
        
        if "error" in simulation:
            return simulation
        
        # Analyze the schedule for insights
        schedule = simulation['daily_schedule']
        
        # Find patterns
        morning_stress = sum(task['stress_level'] for task in schedule[:3]) / 3
        afternoon_stress = sum(task['stress_level'] for task in schedule[3:6]) / 3 if len(schedule) > 6 else 0
        evening_stress = sum(task['stress_level'] for task in schedule[6:]) / len(schedule[6:]) if len(schedule) > 6 else 0
        
        insights = {
            'career_title': simulation['career_title'],
            'daily_patterns': {
                'morning_stress_avg': round(morning_stress, 1),
                'afternoon_stress_avg': round(afternoon_stress, 1),
                'evening_stress_avg': round(evening_stress, 1),
                'most_stressful_period': 'Morning' if morning_stress >= max(afternoon_stress, evening_stress) else 
                                       'Afternoon' if afternoon_stress >= evening_stress else 'Evening'
            },
            'work_characteristics': {
                'total_working_hours': simulation['working_hours']['total_hours'],
                'flexibility': 'High' if 'flexible' in simulation['working_hours'] else 'Medium',
                'physical_demands': 'High' if career_name in ['Doctor', 'IAS Officer'] else 'Low',
                'mental_demands': 'High' if simulation['average_stress_level'] > 3 else 'Medium'
            },
            'career_progression': {
                'entry_barrier': 'High' if 'degree' in simulation['education_required'].lower() else 'Medium',
                'learning_curve': 'Steep' if simulation['average_stress_level'] > 3 else 'Moderate',
                'growth_potential': 'High' if career_name in ['Doctor', 'IAS Officer', 'Software Engineer'] else 'Medium'
            },
            'lifestyle_impact': {
                'work_life_balance_rating': simulation['work_intensity']['work_life_balance_score'],
                'social_impact': 'High' if career_name in ['Doctor', 'IAS Officer', 'Teacher'] else 'Medium',
                'financial_stability': 'High' if 'high' in simulation['salary_range'].lower() or '$' in simulation['salary_range'] else 'Medium'
            }
        }
        
        return insights