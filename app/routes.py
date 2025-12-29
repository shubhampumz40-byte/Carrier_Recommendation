from flask import Blueprint, render_template, request, jsonify, session
from recommender.career_matcher import CareerMatcher
from recommender.personality_test import PersonalityTest
from recommender.explainer import RecommendationExplainer
from recommender.role_model_service import RoleModelService
from recommender.career_comparison import CareerComparison
from recommender.career_simulation import CareerSimulation
import random
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/assessment')
def assessment():
    return render_template('assessment.html')

@main.route('/personality-test')
def personality_test():
    test = PersonalityTest()
    questions = test.get_questions()
    return render_template('personality_test.html', questions=questions)

@main.route('/api/set-preferences', methods=['POST'])
def set_preferences():
    """Set user preferences for region and mode"""
    data = request.json
    session['region'] = data.get('region', 'global')
    session['mode'] = data.get('mode', 'student')
    
    return jsonify({
        'success': True,
        'region': session['region'],
        'mode': session['mode']
    })

@main.route('/api/get-preferences')
def get_preferences():
    """Get current user preferences"""
    return jsonify({
        'region': session.get('region', 'global'),
        'mode': session.get('mode', 'student')
    })

@main.route('/api/recommend', methods=['POST'])
def recommend_careers():
    data = request.json
    
    # Get user preferences
    region = session.get('region', data.get('region', 'global'))
    mode = session.get('mode', data.get('mode', 'student'))
    
    matcher = CareerMatcher(region=region, mode=mode)
    explainer = RecommendationExplainer()
    role_model_service = RoleModelService(region=region)
    
    # Import skills gap analyzer
    from recommender.skills_gap_analyzer import SkillsGapAnalyzer
    skills_analyzer = SkillsGapAnalyzer()
    
    # Get recommendations
    recommendations = matcher.get_recommendations(
        interests=data.get('interests', []),
        skills=data.get('skills', []),
        subjects=data.get('subjects', []),
        personality=data.get('personality', {}),
        experience_level=data.get('experience_level')
    )
    
    # Add explanations and skills gap analysis
    explained_recommendations = []
    for career in recommendations:
        explanation = explainer.explain_recommendation(career, data)
        
        # Perform skills gap analysis
        skills_gap = skills_analyzer.analyze_skills_gap(
            user_skills=data.get('skills', []),
            career_requirements=career,
            user_subjects=data.get('subjects', []),
            user_interests=data.get('interests', [])
        )
        
        explained_recommendations.append({
            'career': career,
            'explanation': explanation,
            'skills_gap': skills_gap
        })
    
    # Get role models for recommended careers
    role_models = role_model_service.get_role_models_for_careers(recommendations)
    
    # Get daily tip based on top career recommendation
    daily_tip = None
    if recommendations:
        daily_tip = role_model_service.get_daily_tip(
            career_focus=recommendations[0]['name'],
            mode=mode
        )
    
    # Get inspiration quote
    inspiration = role_model_service.get_inspiration_quote(
        recommendations[0]['name'] if recommendations else None
    )
    
    # Get region info
    region_info = matcher.get_region_info()
    
    return jsonify({
        'recommendations': explained_recommendations,
        'visualization_data': matcher.get_visualization_data(data),
        'role_models': role_models,
        'daily_tip': daily_tip,
        'inspiration': inspiration,
        'region_info': region_info,
        'mode': mode,
        'region': region
    })

@main.route('/api/personality-result', methods=['POST'])
def personality_result():
    answers = request.json.get('answers', [])
    test = PersonalityTest()
    result = test.calculate_personality(answers)
    return jsonify(result)

@main.route('/results')
def results():
    return render_template('results.html')

@main.route('/visualization-demo')
def visualization_demo():
    return render_template('visualization_demo.html')

@main.route('/api/daily-tip')
def get_daily_tip():
    region = session.get('region', request.args.get('region', 'global'))
    mode = session.get('mode', request.args.get('mode', 'student'))
    
    role_model_service = RoleModelService(region=region)
    career_focus = request.args.get('career')
    user_id = request.args.get('user_id', 'anonymous')
    
    tip = role_model_service.get_daily_tip(career_focus, user_id, mode)
    inspiration = role_model_service.get_inspiration_quote(career_focus)
    
    return jsonify({
        'tip': tip,
        'inspiration': inspiration,
        'region': region,
        'mode': mode
    })

@main.route('/api/role-models')
def get_role_models():
    region = session.get('region', request.args.get('region', 'global'))
    role_model_service = RoleModelService(region=region)
    career = request.args.get('career')
    
    if career:
        models = role_model_service.get_role_models_for_career(career)
    else:
        models = role_model_service.role_models
    
    return jsonify({
        'role_models': models,
        'region': region
    })

@main.route('/api/weekly-tips')
def get_weekly_tips():
    region = session.get('region', request.args.get('region', 'global'))
    mode = session.get('mode', request.args.get('mode', 'student'))
    
    role_model_service = RoleModelService(region=region)
    career_focus = request.args.get('career')
    
    tips = role_model_service.get_weekly_tips(career_focus, mode)
    return jsonify({
        'tips': tips,
        'region': region,
        'mode': mode
    })

@main.route('/api/careers-by-region')
def get_careers_by_region():
    """Get available careers for a specific region"""
    region = request.args.get('region', 'global')
    matcher = CareerMatcher(region=region)
    
    return jsonify({
        'careers': matcher.careers_data,
        'region_info': matcher.get_region_info(),
        'region': region
    })

@main.route('/role-models')
def role_models_page():
    return render_template('role_models.html')

@main.route('/daily-tips')
def daily_tips_page():
    return render_template('daily_tips.html')

@main.route('/mode-selection')
def mode_selection():
    return render_template('mode_selection.html')

@main.route('/trending-careers')
def trending_careers():
    return render_template('trending_careers.html')

@main.route('/api/trending-careers')
def get_trending_careers():
    """Get trending careers data for radar visualization"""
    region = session.get('region', request.args.get('region', 'global'))
    
    try:
        with open('data/trending_careers.json', 'r', encoding='utf-8') as f:
            trending_data = json.load(f)
        
        careers = trending_data['trending_careers_2025_2035'][region]
        categories = trending_data['trend_categories']
        time_horizons = trending_data['time_horizons']
        
        # Prepare radar chart data
        radar_data = {
            'careers': careers,
            'categories': categories,
            'time_horizons': time_horizons,
            'region': region
        }
        
        return jsonify(radar_data)
        
    except FileNotFoundError:
        return jsonify({'error': 'Trending careers data not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/career-reality-check/<path:career_name>')
def get_career_reality_check(career_name):
    """Get realistic career insights including challenges, risks, and backup options"""
    try:
        # URL decode the career name
        from urllib.parse import unquote
        career_name = unquote(career_name)
        
        with open('data/career_reality_check.json', 'r', encoding='utf-8') as f:
            reality_data = json.load(f)
        
        career_data = reality_data['career_reality_data'].get(career_name)
        if not career_data:
            # Try to find a case-insensitive match
            for key in reality_data['career_reality_data'].keys():
                if key.lower() == career_name.lower():
                    career_data = reality_data['career_reality_data'][key]
                    career_name = key
                    break
        
        if not career_data:
            available_careers = list(reality_data['career_reality_data'].keys())
            return jsonify({
                'error': f'Career data not found for "{career_name}"',
                'available_careers': available_careers
            }), 404
        
        # Add general insights
        response_data = {
            'career_name': career_name,
            'reality_check': career_data,
            'general_insights': reality_data['general_insights']
        }
        
        return jsonify(response_data)
        
    except FileNotFoundError:
        return jsonify({'error': 'Career reality data not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/skills-gap-analysis', methods=['POST'])
def analyze_skills_gap():
    """Analyze skills gap for a specific career"""
    data = request.json
    
    try:
        from recommender.skills_gap_analyzer import SkillsGapAnalyzer
        skills_analyzer = SkillsGapAnalyzer()
        
        # Get career data
        region = session.get('region', data.get('region', 'global'))
        matcher = CareerMatcher(region=region)
        
        career_name = data.get('career_name')
        if not career_name:
            return jsonify({'error': 'Career name is required'}), 400
        
        # Find the career in the database
        career_data = None
        for career in matcher.careers_data:
            if career['name'].lower() == career_name.lower():
                career_data = career
                break
        
        if not career_data:
            return jsonify({'error': 'Career not found'}), 404
        
        # Perform skills gap analysis
        skills_gap = skills_analyzer.analyze_skills_gap(
            user_skills=data.get('user_skills', []),
            career_requirements=career_data,
            user_subjects=data.get('user_subjects', []),
            user_interests=data.get('user_interests', [])
        )
        
        return jsonify(skills_gap)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/skills-gap-analyzer')
def skills_gap_analyzer_page():
    return render_template('skills_gap_analyzer.html')

@main.route('/career-reality-check')
def career_reality_check():
    return render_template('career_reality_check.html')

@main.route('/career-comparison')
def career_comparison():
    return render_template('career_comparison.html')

@main.route('/api/career-comparison/careers')
def get_careers_for_comparison():
    """Get available careers for comparison"""
    region = request.args.get('region', 'global')
    
    try:
        comparison_service = CareerComparison()
        careers = comparison_service.get_available_careers(region)
        
        return jsonify({
            'careers': careers,
            'region': region
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/career-comparison/compare', methods=['POST'])
def compare_careers():
    """Compare multiple careers across key dimensions"""
    data = request.json
    
    try:
        comparison_service = CareerComparison()
        
        careers = data.get('careers', [])
        region = data.get('region', 'global')
        
        if len(careers) < 2:
            return jsonify({'error': 'Please select at least 2 careers to compare'}), 400
        
        if len(careers) > 5:
            return jsonify({'error': 'Maximum 5 careers can be compared at once'}), 400
        
        comparison_result = comparison_service.compare_careers(careers, region)
        
        return jsonify(comparison_result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/career-comparison/detailed', methods=['POST'])
def detailed_career_comparison():
    """Get detailed side-by-side comparison of two careers"""
    data = request.json
    
    try:
        comparison_service = CareerComparison()
        
        career1 = data.get('career1')
        career2 = data.get('career2')
        region = data.get('region', 'global')
        
        if not career1 or not career2:
            return jsonify({'error': 'Both careers must be specified'}), 400
        
        comparison_result = comparison_service.get_detailed_comparison(career1, career2, region)
        
        return jsonify(comparison_result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/career-simulation')
def career_simulation():
    return render_template('career_simulation.html')

@main.route('/api/career-simulation/careers')
def get_simulation_careers():
    """Get available careers for simulation"""
    try:
        simulation_service = CareerSimulation()
        careers = simulation_service.get_available_careers()
        
        return jsonify({
            'careers': careers
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/career-simulation/<path:career_name>')
def get_career_simulation(career_name):
    """Get complete simulation data for a specific career"""
    try:
        # URL decode the career name
        from urllib.parse import unquote
        career_name = unquote(career_name)
        
        region = request.args.get('region', 'global')
        
        simulation_service = CareerSimulation()
        simulation_data = simulation_service.get_career_simulation(career_name, region)
        
        return jsonify(simulation_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/career-simulation/summary/<path:career_name>')
def get_simulation_summary(career_name):
    """Get condensed summary of career simulation"""
    try:
        from urllib.parse import unquote
        career_name = unquote(career_name)
        
        region = request.args.get('region', 'global')
        
        simulation_service = CareerSimulation()
        summary = simulation_service.get_simulation_summary(career_name, region)
        
        return jsonify(summary)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/career-simulation/insights/<path:career_name>')
def get_career_insights(career_name):
    """Get detailed insights and analysis for a career"""
    try:
        from urllib.parse import unquote
        career_name = unquote(career_name)
        
        region = request.args.get('region', 'global')
        
        simulation_service = CareerSimulation()
        insights = simulation_service.get_career_insights(career_name, region)
        
        return jsonify(insights)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500