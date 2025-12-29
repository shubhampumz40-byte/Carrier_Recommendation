import json

class PersonalityTest:
    def __init__(self):
        self.questions = self._load_questions()
        self.personality_types = self._load_personality_types()
    
    def _load_questions(self):
        """Load personality test questions"""
        return [
            {
                "id": 1,
                "question": "I prefer working in teams rather than alone",
                "dimension": "extraversion",
                "weight": 1
            },
            {
                "id": 2,
                "question": "I enjoy meeting new people and making connections",
                "dimension": "extraversion",
                "weight": 1
            },
            {
                "id": 3,
                "question": "I prefer concrete facts over abstract theories",
                "dimension": "sensing",
                "weight": 1
            },
            {
                "id": 4,
                "question": "I focus on details rather than the big picture",
                "dimension": "sensing",
                "weight": 1
            },
            {
                "id": 5,
                "question": "I make decisions based on logic rather than feelings",
                "dimension": "thinking",
                "weight": 1
            },
            {
                "id": 6,
                "question": "I analyze problems objectively without emotional bias",
                "dimension": "thinking",
                "weight": 1
            },
            {
                "id": 7,
                "question": "I prefer to plan ahead rather than be spontaneous",
                "dimension": "judging",
                "weight": 1
            },
            {
                "id": 8,
                "question": "I like to have things organized and structured",
                "dimension": "judging",
                "weight": 1
            },
            {
                "id": 9,
                "question": "I get energized by social interactions",
                "dimension": "extraversion",
                "weight": 1
            },
            {
                "id": 10,
                "question": "I trust my intuition when making decisions",
                "dimension": "intuition",
                "weight": 1
            },
            {
                "id": 11,
                "question": "I consider how decisions affect people's feelings",
                "dimension": "feeling",
                "weight": 1
            },
            {
                "id": 12,
                "question": "I adapt easily to changing situations",
                "dimension": "perceiving",
                "weight": 1
            }
        ]
    
    def _load_personality_types(self):
        """Load personality type descriptions"""
        return {
            "INTJ": {
                "name": "The Architect",
                "traits": ["analytical", "strategic", "independent"],
                "careers": ["Software Engineer", "Data Scientist", "Research Scientist"],
                "description": "Strategic thinkers who love complex problems"
            },
            "ENFP": {
                "name": "The Campaigner", 
                "traits": ["creative", "enthusiastic", "collaborative"],
                "careers": ["UX Designer", "Marketing Manager", "Teacher"],
                "description": "Creative and enthusiastic people-focused individuals"
            },
            "ISTJ": {
                "name": "The Logistician",
                "traits": ["detail_oriented", "organized", "reliable"],
                "careers": ["Accountant", "Project Manager", "Engineer"],
                "description": "Practical and fact-minded, reliable individuals"
            },
            "ESTP": {
                "name": "The Entrepreneur",
                "traits": ["outgoing", "adaptable", "practical"],
                "careers": ["Sales Manager", "Marketing Manager", "Consultant"],
                "description": "Energetic and adaptable, great at improvising"
            }
        }
    
    def get_questions(self):
        """Return personality test questions"""
        return self.questions
    
    def calculate_personality(self, answers):
        """Calculate personality type from answers"""
        # Initialize dimension scores
        scores = {
            "extraversion": 0,
            "introversion": 0,
            "sensing": 0,
            "intuition": 0,
            "thinking": 0,
            "feeling": 0,
            "judging": 0,
            "perceiving": 0
        }
        
        # Calculate scores based on answers
        for i, answer in enumerate(answers):
            if i < len(self.questions):
                question = self.questions[i]
                dimension = question["dimension"]
                weight = question["weight"]
                
                # Answer scale: 1-5 (strongly disagree to strongly agree)
                if dimension in ["extraversion", "sensing", "thinking", "judging"]:
                    scores[dimension] += answer * weight
                    # Add opposite score
                    opposite = self._get_opposite_dimension(dimension)
                    scores[opposite] += (6 - answer) * weight
        
        # Determine personality type
        personality_type = ""
        personality_type += "E" if scores["extraversion"] > scores["introversion"] else "I"
        personality_type += "S" if scores["sensing"] > scores["intuition"] else "N"
        personality_type += "T" if scores["thinking"] > scores["feeling"] else "F"
        personality_type += "J" if scores["judging"] > scores["perceiving"] else "P"
        
        # Get personality description
        type_info = self.personality_types.get(personality_type, {
            "name": "Unique Type",
            "traits": ["unique", "individual"],
            "careers": ["Various careers"],
            "description": "A unique personality combination"
        })
        
        return {
            "type": personality_type,
            "name": type_info["name"],
            "traits": type_info["traits"],
            "suggested_careers": type_info["careers"],
            "description": type_info["description"],
            "scores": scores
        }
    
    def _get_opposite_dimension(self, dimension):
        """Get the opposite dimension"""
        opposites = {
            "extraversion": "introversion",
            "sensing": "intuition", 
            "thinking": "feeling",
            "judging": "perceiving"
        }
        return opposites.get(dimension, dimension)