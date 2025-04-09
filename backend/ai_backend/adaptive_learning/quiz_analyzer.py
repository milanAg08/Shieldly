# backend/ai_backend/adaptive_learning/quiz_analyzer.py

from extensions import db
from ai_backend.models.progress import Progress
from ai_backend.models.user import User
from datetime import datetime

class QuizAnalyzer:
    """Analyzes quiz results and adapts learning content accordingly"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.user = User.query.get(user_id)
        if not self.user:
            raise ValueError(f"User with ID {user_id} not found")
    
    def analyze_quiz_result(self, module_id, score, time_taken):
        """
        Analyze a quiz result and update user progress
        
        Args:
            module_id (str): The module identifier
            score (float): Score as a percentage (0-100)
            time_taken (int): Time taken in seconds
        
        Returns:
            dict: Analysis results and recommendations
        """
        # Find or create progress record
        progress = Progress.query.filter_by(
            user_id=self.user_id,
            module_id=module_id
        ).first()
        
        if not progress:
            progress = Progress(
                user_id=self.user_id,
                module_id=module_id,
                completion_percentage=0.0,
                time_spent=0,
                last_activity=datetime.utcnow()
            )
            db.session.add(progress)
        
        # Update progress with quiz results
        progress.quiz_score = score
        progress.quiz_time_taken = time_taken
        progress.last_activity = datetime.utcnow()
        
        # Calculate new completion percentage based on quiz score
        # This is a simplified approach - in a real system you'd have more factors
        if score >= 80:
            # If score is high, mark module as completed
            progress.completion_percentage = 100.0
        elif score >= 60:
            # If score is medium, mark as mostly completed
            progress.completion_percentage = max(progress.completion_percentage, 75.0)
        else:
            # If score is low, only mark as partially completed
            progress.completion_percentage = max(progress.completion_percentage, 50.0)
        
        db.session.commit()
        
        # Generate recommendations based on performance
        recommendations = self._generate_recommendations(score, time_taken)
        
        # Determine next module recommendation
        next_module = self._recommend_next_module(module_id, score)
        
        return {
            'score': score,
            'completion_percentage': progress.completion_percentage,
            'mastery_level': self._determine_mastery_level(score),
            'recommendations': recommendations,
            'next_module': next_module
        }
    
    def _determine_mastery_level(self, score):
        """Determine mastery level based on score"""
        if score >= 90:
            return "expert"
        elif score >= 75:
            return "proficient"
        elif score >= 60:
            return "intermediate"
        elif score >= 40:
            return "beginner"
        else:
            return "novice"
    
    def _generate_recommendations(self, score, time_taken):
        """
        Generate learning recommendations based on quiz performance
        
        Returns:
            list: List of recommendation strings
        """
        recommendations = []
        
        # Recommendations based on score
        if score < 40:
            recommendations.append("Review the core concepts in this module again")
            recommendations.append("Try the simplified version of this material")
        elif score < 60:
            recommendations.append("Focus on the specific areas you missed in the quiz")
            recommendations.append("Consider reviewing the key definitions")
        elif score < 75:
            recommendations.append("Practice with additional examples to strengthen understanding")
        else:
            recommendations.append("You're doing well! Consider exploring the advanced concepts")
        
        # Recommendations based on time taken
        # Assuming an average completion time of 120 seconds
        avg_time = 120
        if time_taken > (avg_time * 1.5) and score < 75:
            # Took longer than expected and low score
            recommendations.append("Try breaking down the material into smaller chunks")
        elif time_taken < (avg_time * 0.5) and score < 60:
            # Very quick but low score
            recommendations.append("Consider spending more time on each question")
        
        return recommendations
    
    def _recommend_next_module(self, current_module_id, score):
        """
        Recommend the next module based on current module and performance
        
        Returns:
            str: Module ID for recommended next module
        """
        # This would normally use a predefined learning path or curriculum map
        # For demonstration, we'll use a simple module naming convention
        
        # Extract module number if format is like "module_1"
        import re
        match = re.match(r'module_(\d+)', current_module_id)
        
        if match:
            module_num = int(match.group(1))
            
            if score < 50:
                # If score is low, recommend staying on current module
                return f"module_{module_num}"
            else:
                # Move to next module
                return f"module_{module_num + 1}"
        
        # Default recommendation if module ID format doesn't match expected pattern
        return "next_recommended_module"
    
    def get_learning_path(self):
        """
        Generate personalized learning path based on user's progress history
        
        Returns:
            list: Ordered list of module IDs representing recommended path
        """
        # Get all progress records for user
        progress_records = Progress.query.filter_by(user_id=self.user_id).all()
        
        # Create dictionary of module completion percentages
        module_completion = {record.module_id: record.completion_percentage for record in progress_records}
        
        # Get all incomplete modules (less than 80% complete)
        incomplete_modules = [
            module_id for module_id, percentage in module_completion.items()
            if percentage < 80.0
        ]
        
        # Get modules that haven't been started
        # This would normally query a curriculum database
        # For demonstration, we'll assume modules are named module_1, module_2, etc.
        existing_modules = set(module_completion.keys())
        all_modules = {f"module_{i}" for i in range(1, 11)}  # Assuming 10 modules
        unstarted_modules = all_modules - existing_modules
        
        # Create learning path: first incomplete modules, then unstarted ones
        learning_path = incomplete_modules + list(unstarted_modules)
        
        return learning_path