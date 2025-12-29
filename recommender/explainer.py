class RecommendationExplainer:
    def __init__(self):
        pass
    
    def explain_recommendation(self, career, user_data):
        """Generate explanation for why a career was recommended"""
        explanation = {
            "overall_match": 0,
            "reasons": [],
            "skill_gaps": [],
            "strengths": []
        }
        
        # Calculate detailed matches
        interests_match = self._explain_interests_match(career, user_data.get('interests', []))
        skills_match = self._explain_skills_match(career, user_data.get('skills', []))
        subjects_match = self._explain_subjects_match(career, user_data.get('subjects', []))
        personality_match = self._explain_personality_match(career, user_data.get('personality', {}))
        
        # Combine explanations
        explanation["reasons"].extend(interests_match["reasons"])
        explanation["reasons"].extend(skills_match["reasons"])
        explanation["reasons"].extend(subjects_match["reasons"])
        explanation["reasons"].extend(personality_match["reasons"])
        
        explanation["skill_gaps"] = skills_match["gaps"]
        explanation["strengths"] = interests_match["strengths"] + skills_match["strengths"]
        
        # Calculate overall match percentage
        total_score = (
            interests_match["score"] * 0.4 +
            skills_match["score"] * 0.35 +
            subjects_match["score"] * 0.15 +
            personality_match["score"] * 0.1
        )
        explanation["overall_match"] = int(total_score * 100)
        
        return explanation
    
    def _explain_interests_match(self, career, user_interests):
        """Explain how interests match the career"""
        career_interests = set(career.get("interests", []))
        user_interests_set = set(user_interests)
        
        matched_interests = career_interests & user_interests_set
        score = len(matched_interests) / max(len(career_interests), 1)
        
        reasons = []
        strengths = []
        
        if matched_interests:
            reasons.append(f"Your interests in {', '.join(matched_interests)} align well with this career")
            strengths.extend(list(matched_interests))
        
        if len(matched_interests) >= len(career_interests) * 0.7:
            reasons.append("Strong interest alignment - you share most key interests for this field")
        elif len(matched_interests) >= len(career_interests) * 0.4:
            reasons.append("Good interest match - several of your interests align with this career")
        
        return {
            "score": score,
            "reasons": reasons,
            "strengths": strengths
        }
    
    def _explain_skills_match(self, career, user_skills):
        """Explain how skills match the career requirements"""
        required_skills = set(career.get("required_skills", []))
        user_skills_set = set(user_skills)
        
        matched_skills = required_skills & user_skills_set
        missing_skills = required_skills - user_skills_set
        
        score = len(matched_skills) / max(len(required_skills), 1)
        
        reasons = []
        gaps = list(missing_skills)
        strengths = list(matched_skills)
        
        if matched_skills:
            reasons.append(f"You already have {len(matched_skills)} out of {len(required_skills)} key skills: {', '.join(matched_skills)}")
        
        if missing_skills:
            reasons.append(f"Skills to develop: {', '.join(missing_skills)}")
        
        if score >= 0.7:
            reasons.append("Excellent skill match - you have most required skills")
        elif score >= 0.4:
            reasons.append("Good skill foundation - some development needed")
        else:
            reasons.append("Significant skill development opportunity")
        
        return {
            "score": score,
            "reasons": reasons,
            "gaps": gaps,
            "strengths": strengths
        }
    
    def _explain_subjects_match(self, career, user_subjects):
        """Explain how academic subjects relate to the career"""
        career_subjects = set(career.get("subjects", []))
        user_subjects_set = set(user_subjects)
        
        matched_subjects = career_subjects & user_subjects_set
        score = len(matched_subjects) / max(len(career_subjects), 1) if career_subjects else 0.5
        
        reasons = []
        
        if matched_subjects:
            reasons.append(f"Your background in {', '.join(matched_subjects)} provides a strong foundation")
        
        if score >= 0.6:
            reasons.append("Strong academic preparation for this field")
        elif score >= 0.3:
            reasons.append("Some relevant academic background")
        
        return {
            "score": score,
            "reasons": reasons
        }
    
    def _explain_personality_match(self, career, personality_data):
        """Explain how personality traits match the career"""
        career_traits = set(career.get("personality_traits", []))
        user_traits = set(personality_data.get("traits", []))
        
        matched_traits = career_traits & user_traits
        score = len(matched_traits) / max(len(career_traits), 1)
        
        reasons = []
        
        if matched_traits:
            reasons.append(f"Your {', '.join(matched_traits)} personality traits fit well with this career")
        
        if score >= 0.6:
            reasons.append("Strong personality-career alignment")
        elif score >= 0.3:
            reasons.append("Some personality traits align with this career")
        
        return {
            "score": score,
            "reasons": reasons
        }