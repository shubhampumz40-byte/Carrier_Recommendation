#!/usr/bin/env python3
"""
Demo script to test the Career Recommender functionality
"""

from recommender.career_matcher import CareerMatcher
from recommender.personality_test import PersonalityTest
from recommender.explainer import RecommendationExplainer

def test_career_matching():
    """Test the career matching functionality"""
    print("🔍 Testing Career Matching System...")
    print("=" * 50)
    
    # Initialize the matcher
    matcher = CareerMatcher()
    explainer = RecommendationExplainer()
    
    # Sample user profile
    sample_profile = {
        'interests': ['technology', 'problem_solving', 'creativity'],
        'skills': ['programming', 'logical_thinking', 'design'],
        'subjects': ['computer_science', 'mathematics'],
        'personality': {'traits': ['analytical', 'creative']}
    }
    
    print(f"📋 Sample User Profile:")
    print(f"   Interests: {', '.join(sample_profile['interests'])}")
    print(f"   Skills: {', '.join(sample_profile['skills'])}")
    print(f"   Subjects: {', '.join(sample_profile['subjects'])}")
    print(f"   Personality: {', '.join(sample_profile['personality']['traits'])}")
    print()
    
    # Get recommendations
    recommendations = matcher.get_recommendations(
        interests=sample_profile['interests'],
        skills=sample_profile['skills'],
        subjects=sample_profile['subjects'],
        personality=sample_profile['personality']
    )
    
    print("🎯 Top Career Recommendations:")
    print("-" * 30)
    
    for i, career in enumerate(recommendations[:3], 1):
        explanation = explainer.explain_recommendation(career, sample_profile)
        
        print(f"{i}. {career['name']} ({explanation['overall_match']}% match)")
        print(f"   💰 Salary: {career['median_salary']}")
        print(f"   📈 Growth: {career['growth_rate']}")
        print(f"   📝 Description: {career['description']}")
        
        if explanation['reasons']:
            print(f"   ✅ Why it matches:")
            for reason in explanation['reasons'][:2]:  # Show top 2 reasons
                print(f"      • {reason}")
        
        if explanation['skill_gaps']:
            print(f"   📚 Skills to develop: {', '.join(explanation['skill_gaps'][:3])}")
        
        print()

def test_personality_test():
    """Test the personality test functionality"""
    print("🧠 Testing Personality Assessment...")
    print("=" * 50)
    
    # Initialize personality test
    test = PersonalityTest()
    
    # Sample answers (1-5 scale)
    sample_answers = [4, 3, 2, 4, 5, 4, 3, 4, 5, 2, 3, 4]  # 12 answers
    
    print(f"📊 Sample Test Answers: {sample_answers}")
    print()
    
    # Calculate personality
    result = test.calculate_personality(sample_answers)
    
    print(f"🎭 Personality Result:")
    print(f"   Type: {result['type']} - {result['name']}")
    print(f"   Description: {result['description']}")
    print(f"   Key Traits: {', '.join(result['traits'])}")
    print(f"   Suggested Careers: {', '.join(result['suggested_careers'])}")
    print()
    
    print(f"📈 Dimension Scores:")
    for dimension, score in result['scores'].items():
        print(f"   {dimension.capitalize()}: {score}")
    print()

def test_visualization_data():
    """Test visualization data generation"""
    print("📊 Testing Visualization Data...")
    print("=" * 50)
    
    matcher = CareerMatcher()
    
    sample_data = {
        'interests': ['technology', 'data'],
        'skills': ['programming', 'analysis'],
        'subjects': ['computer_science'],
        'personality': {'traits': ['analytical']}
    }
    
    viz_data = matcher.get_visualization_data(sample_data)
    
    print(f"🌐 Network Visualization Data:")
    print(f"   Nodes: {len(viz_data['nodes'])}")
    print(f"   Links: {len(viz_data['links'])}")
    
    for node in viz_data['nodes']:
        print(f"   • {node['name']} ({node['type']})")
    
    print()

if __name__ == "__main__":
    print("🚀 Career Recommender System Demo")
    print("=" * 60)
    print()
    
    try:
        test_career_matching()
        test_personality_test()
        test_visualization_data()
        
        print("✅ All tests completed successfully!")
        print()
        print("🌐 To run the web application:")
        print("   python run.py")
        print("   Then open: http://localhost:5000")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()