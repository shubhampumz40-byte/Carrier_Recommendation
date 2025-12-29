"""
Failure & Dropout Warning System
Analyzes academic consistency, interest stability, and stress tolerance
to predict career success and provide early warnings
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple
import statistics

class FailureWarningSystem:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.criteria_data = self._load_criteria_data()
        
    def _load_criteria_data(self) -> Dict:
        """Load failure warning criteria from JSON file"""
        criteria_path = os.path.join(self.data_dir, 'failure_warning_criteria.json')
        if os.path.exists(criteria_path):
            with open(criteria_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def analyze_student_risk(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive risk analysis for a student
        
        Args:
            student_data: Dictionary containing student information
                - academic_history: List of grades/performance data
                - interest_history: List of career interests over time
                - stress_indicators: Dictionary of stress-related responses
                - demographic_info: Age, education level, etc.
                - career_preferences: Current career choices
        
        Returns:
            Comprehensive risk assessment with warnings and recommendations
        """
        
        # Analyze each dimension
        academic_risk = self._analyze_academic_consistency(student_data.get('academic_history', {}))
        interest_risk = self._analyze_interest_stability(student_data.get('interest_history', {}))
        stress_risk = self._analyze_stress_tolerance(student_data.get('stress_indicators', {}))
        
        # Calculate overall risk score
        overall_risk = self._calculate_overall_risk(academic_risk, interest_risk, stress_risk)
        
        # Get career-specific warnings
        career_warnings = self._get_career_specific_warnings(
            student_data.get('career_preferences', []),
            overall_risk
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(academic_risk, interest_risk, stress_risk)
        
        return {
            'overall_risk_score': overall_risk['score'],
            'overall_risk_level': overall_risk['level'],
            'risk_breakdown': {
                'academic_consistency': academic_risk,
                'interest_stability': interest_risk,
                'stress_tolerance': stress_risk
            },
            'career_warnings': career_warnings,
            'recommendations': recommendations,
            'intervention_strategies': self._get_intervention_strategies(overall_risk),
            'success_probability': self._calculate_success_probability(overall_risk),
            'alternative_paths': self._suggest_alternative_paths(overall_risk, student_data)
        }
    
    def _analyze_academic_consistency(self, academic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze academic performance patterns"""
        criteria = self.criteria_data['failure_warning_criteria']['academic_consistency']
        risk_score = 0.0
        risk_factors_found = []
        
        # Analyze grade trends
        grades = academic_data.get('grades', [])
        if grades and len(grades) >= 2:
            grade_trend = self._calculate_grade_trend(grades)
            if grade_trend < -0.1:  # 10% decline
                risk_score += 0.3
                risk_factors_found.append("Declining academic performance")
        
        # Analyze attendance
        attendance = academic_data.get('attendance_rate', 100)
        if attendance < 75:
            risk_score += 0.2
            risk_factors_found.append("Poor attendance record")
        
        # Analyze study habits
        study_consistency = academic_data.get('study_consistency_score', 5)  # 1-10 scale
        if study_consistency < 4:
            risk_score += 0.25
            risk_factors_found.append("Inconsistent study habits")
        
        # Analyze subject performance
        subject_failures = academic_data.get('failed_subjects', 0)
        if subject_failures > 0:
            risk_score += min(0.25, subject_failures * 0.1)
            risk_factors_found.append(f"Failed {subject_failures} subjects")
        
        # Determine risk level
        risk_level = self._get_risk_level(risk_score, criteria['warning_levels'])
        
        return {
            'score': min(1.0, risk_score),
            'level': risk_level,
            'risk_factors': risk_factors_found,
            'recommendations': criteria['warning_levels'][risk_level]['recommendations']
        }
    
    def _analyze_interest_stability(self, interest_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze career interest consistency and depth"""
        criteria = self.criteria_data['failure_warning_criteria']['interest_stability']
        risk_score = 0.0
        risk_factors_found = []
        
        # Analyze career changes
        career_changes = interest_data.get('career_changes_count', 0)
        if career_changes >= 3:
            risk_score += 0.35
            risk_factors_found.append(f"Changed career goals {career_changes} times")
        
        # Analyze exploration depth
        research_depth = interest_data.get('career_research_score', 5)  # 1-10 scale
        if research_depth < 4:
            risk_score += 0.25
            risk_factors_found.append("Limited career research")
        
        # Analyze external pressure
        external_influence = interest_data.get('external_pressure_score', 3)  # 1-10 scale
        if external_influence > 7:
            risk_score += 0.2
            risk_factors_found.append("High external pressure in career choice")
        
        # Analyze passion indicators
        passion_score = interest_data.get('passion_indicators_score', 5)  # 1-10 scale
        if passion_score < 4:
            risk_score += 0.2
            risk_factors_found.append("Low passion for chosen field")
        
        # Determine risk level
        risk_level = self._get_risk_level(risk_score, criteria['warning_levels'])
        
        return {
            'score': min(1.0, risk_score),
            'level': risk_level,
            'risk_factors': risk_factors_found,
            'recommendations': criteria['warning_levels'][risk_level]['recommendations']
        }
    
    def _analyze_stress_tolerance(self, stress_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze stress tolerance and coping mechanisms"""
        criteria = self.criteria_data['failure_warning_criteria']['stress_tolerance']
        risk_score = 0.0
        risk_factors_found = []
        
        # Analyze anxiety levels
        anxiety_score = stress_data.get('anxiety_level', 3)  # 1-10 scale
        if anxiety_score > 7:
            risk_score += 0.3
            risk_factors_found.append("High anxiety levels")
        
        # Analyze pressure response
        pressure_performance = stress_data.get('pressure_performance_score', 5)  # 1-10 scale
        if pressure_performance < 4:
            risk_score += 0.25
            risk_factors_found.append("Poor performance under pressure")
        
        # Analyze coping mechanisms
        coping_skills = stress_data.get('coping_skills_score', 5)  # 1-10 scale
        if coping_skills < 4:
            risk_score += 0.25
            risk_factors_found.append("Lack of healthy coping mechanisms")
        
        # Analyze resilience
        resilience_score = stress_data.get('resilience_score', 5)  # 1-10 scale
        if resilience_score < 4:
            risk_score += 0.2
            risk_factors_found.append("Low resilience to setbacks")
        
        # Determine risk level
        risk_level = self._get_risk_level(risk_score, criteria['warning_levels'])
        
        return {
            'score': min(1.0, risk_score),
            'level': risk_level,
            'risk_factors': risk_factors_found,
            'recommendations': criteria['warning_levels'][risk_level]['recommendations']
        }
    
    def _calculate_grade_trend(self, grades: List[float]) -> float:
        """Calculate grade trend (positive = improving, negative = declining)"""
        if len(grades) < 2:
            return 0.0
        
        # Simple linear trend calculation
        x = list(range(len(grades)))
        y = grades
        
        n = len(grades)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x[i] * y[i] for i in range(n))
        sum_x2 = sum(x[i] ** 2 for i in range(n))
        
        if n * sum_x2 - sum_x ** 2 == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        return slope / max(grades)  # Normalize by max grade
    
    def _get_risk_level(self, score: float, warning_levels: Dict) -> str:
        """Determine risk level based on score"""
        for level, data in warning_levels.items():
            min_score, max_score = data['score_range']
            if min_score <= score <= max_score:
                return level
        return 'moderate_risk'  # Default
    
    def _calculate_overall_risk(self, academic_risk: Dict, interest_risk: Dict, stress_risk: Dict) -> Dict[str, Any]:
        """Calculate overall risk score and level"""
        # Weighted average of risk scores
        weights = {'academic': 0.4, 'interest': 0.3, 'stress': 0.3}
        
        overall_score = (
            academic_risk['score'] * weights['academic'] +
            interest_risk['score'] * weights['interest'] +
            stress_risk['score'] * weights['stress']
        )
        
        # Determine overall risk level
        if overall_score <= 0.3:
            level = 'low_risk'
        elif overall_score <= 0.6:
            level = 'moderate_risk'
        else:
            level = 'high_risk'
        
        return {
            'score': overall_score,
            'level': level,
            'primary_concerns': self._identify_primary_concerns(academic_risk, interest_risk, stress_risk)
        }
    
    def _identify_primary_concerns(self, academic_risk: Dict, interest_risk: Dict, stress_risk: Dict) -> List[str]:
        """Identify the primary areas of concern"""
        concerns = []
        
        if academic_risk['score'] > 0.5:
            concerns.append('Academic Performance')
        if interest_risk['score'] > 0.5:
            concerns.append('Career Interest Stability')
        if stress_risk['score'] > 0.5:
            concerns.append('Stress Management')
        
        return concerns if concerns else ['Overall Career Readiness']
    
    def _get_career_specific_warnings(self, career_preferences: List[str], overall_risk: Dict) -> List[Dict]:
        """Generate warnings for specific career choices"""
        warnings = []
        career_risk_mapping = self.criteria_data.get('career_risk_mapping', {})
        
        for career in career_preferences:
            # Find career in risk mapping
            career_info = None
            for category in career_risk_mapping.values():
                if isinstance(category, list):
                    for career_data in category:
                        if career_data['career'] == career:
                            career_info = career_data
                            break
            
            if career_info:
                warning = {
                    'career': career,
                    'career_stress_level': career_info['stress_level'],
                    'dropout_rate': career_info['dropout_rate'],
                    'common_failure_reasons': career_info['common_reasons'],
                    'risk_assessment': self._assess_career_fit(career_info, overall_risk),
                    'specific_warnings': self._generate_career_warnings(career_info, overall_risk)
                }
                warnings.append(warning)
        
        return warnings
    
    def _assess_career_fit(self, career_info: Dict, overall_risk: Dict) -> str:
        """Assess how well the student fits the career based on risk analysis"""
        career_stress = career_info['stress_level']
        student_risk = overall_risk['score']
        
        if student_risk > 0.6 and career_stress > 3.0:
            return 'High Risk - Not Recommended'
        elif student_risk > 0.4 and career_stress > 3.5:
            return 'Moderate Risk - Proceed with Caution'
        elif student_risk < 0.3:
            return 'Good Fit - Low Risk'
        else:
            return 'Moderate Fit - Monitor Progress'
    
    def _generate_career_warnings(self, career_info: Dict, overall_risk: Dict) -> List[str]:
        """Generate specific warnings for a career choice"""
        warnings = []
        
        if overall_risk['score'] > 0.5:
            warnings.append(f"High dropout rate ({career_info['dropout_rate']}) in this field")
            warnings.append("Your risk profile suggests challenges in this career")
        
        if career_info['stress_level'] > 3.0 and overall_risk['score'] > 0.4:
            warnings.append("This is a high-stress career that may not suit your stress tolerance")
        
        return warnings
    
    def _generate_recommendations(self, academic_risk: Dict, interest_risk: Dict, stress_risk: Dict) -> List[str]:
        """Generate personalized recommendations based on risk analysis"""
        recommendations = []
        
        # Academic recommendations
        if academic_risk['score'] > 0.5:
            recommendations.extend([
                "Focus on improving study habits and time management",
                "Consider academic tutoring or support services",
                "Address attendance and engagement issues"
            ])
        
        # Interest recommendations
        if interest_risk['score'] > 0.5:
            recommendations.extend([
                "Spend more time exploring career options through internships",
                "Talk to professionals in your field of interest",
                "Consider career counseling to clarify your interests"
            ])
        
        # Stress recommendations
        if stress_risk['score'] > 0.5:
            recommendations.extend([
                "Learn stress management and relaxation techniques",
                "Consider careers with better work-life balance",
                "Seek counseling for anxiety management"
            ])
        
        return recommendations
    
    def _get_intervention_strategies(self, overall_risk: Dict) -> List[str]:
        """Get intervention strategies based on risk level"""
        strategies = self.criteria_data.get('intervention_strategies', {})
        
        if overall_risk['level'] == 'high_risk':
            return (strategies.get('academic_support', []) + 
                   strategies.get('stress_management', []) + 
                   strategies.get('career_alternatives', []))
        elif overall_risk['level'] == 'moderate_risk':
            return (strategies.get('interest_exploration', []) + 
                   strategies.get('academic_support', [])[:2])
        else:
            return strategies.get('interest_exploration', [])[:2]
    
    def _calculate_success_probability(self, overall_risk: Dict) -> Dict[str, Any]:
        """Calculate probability of career success"""
        risk_score = overall_risk['score']
        
        # Convert risk score to success probability
        success_probability = max(0.1, 1.0 - risk_score)
        
        if success_probability > 0.8:
            outlook = 'Excellent'
        elif success_probability > 0.6:
            outlook = 'Good'
        elif success_probability > 0.4:
            outlook = 'Fair'
        else:
            outlook = 'Challenging'
        
        return {
            'probability': success_probability,
            'percentage': f"{success_probability * 100:.1f}%",
            'outlook': outlook,
            'confidence_level': 'High' if risk_score < 0.3 or risk_score > 0.7 else 'Moderate'
        }
    
    def _suggest_alternative_paths(self, overall_risk: Dict, student_data: Dict) -> List[Dict]:
        """Suggest alternative career paths based on risk analysis"""
        alternatives = []
        
        if overall_risk['score'] > 0.6:
            # High risk - suggest lower stress alternatives
            alternatives.extend([
                {
                    'path': 'Gap Year with Skill Development',
                    'description': 'Take time to build foundational skills and explore interests',
                    'duration': '1 year',
                    'benefits': ['Reduced pressure', 'Skill building', 'Career exploration']
                },
                {
                    'path': 'Community College Start',
                    'description': 'Begin with community college to build academic confidence',
                    'duration': '2 years',
                    'benefits': ['Lower cost', 'Smaller classes', 'Academic support']
                },
                {
                    'path': 'Trade/Vocational Training',
                    'description': 'Consider skilled trades with good job prospects',
                    'duration': '6 months - 2 years',
                    'benefits': ['Hands-on learning', 'Job security', 'Good wages']
                }
            ])
        elif overall_risk['score'] > 0.4:
            # Moderate risk - suggest supportive paths
            alternatives.extend([
                {
                    'path': 'Structured Support Program',
                    'description': 'Enroll in programs with built-in academic and career support',
                    'duration': 'Throughout education',
                    'benefits': ['Mentorship', 'Academic support', 'Career guidance']
                },
                {
                    'path': 'Part-time Study Option',
                    'description': 'Reduce course load to manage stress and improve performance',
                    'duration': 'Extended timeline',
                    'benefits': ['Reduced stress', 'Work experience', 'Better balance']
                }
            ])
        
        return alternatives
    
    def quick_risk_assessment(self, basic_data: Dict[str, Any]) -> Dict[str, Any]:
        """Quick risk assessment with minimal data"""
        risk_indicators = 0
        warnings = []
        
        # Check basic indicators
        if basic_data.get('recent_grade_drop', False):
            risk_indicators += 1
            warnings.append("Recent decline in academic performance")
        
        if basic_data.get('career_uncertainty', False):
            risk_indicators += 1
            warnings.append("Uncertainty about career direction")
        
        if basic_data.get('high_stress_levels', False):
            risk_indicators += 1
            warnings.append("High stress and anxiety levels")
        
        if basic_data.get('external_pressure', False):
            risk_indicators += 1
            warnings.append("External pressure influencing career choice")
        
        # Determine risk level
        if risk_indicators >= 3:
            risk_level = 'high_risk'
        elif risk_indicators >= 2:
            risk_level = 'moderate_risk'
        else:
            risk_level = 'low_risk'
        
        return {
            'risk_level': risk_level,
            'risk_indicators_count': risk_indicators,
            'warnings': warnings,
            'recommendation': 'Complete full assessment for detailed analysis' if risk_indicators > 1 else 'Continue with current path'
        }