# backend/ai_backend/adaptive_learning/user_progress.py

from backend.extensions import db
from backend.ai_backend.models.progress import Progress
from ai_backend.models.user import User
from datetime import datetime, timedelta

class UserProgressTracker:
    """Tracks and analyzes user progress through learning modules"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.user = User.query.get(user_id)
        if not self.user:
            raise ValueError(f"User with ID {user_id} not found")
    
    def track_activity(self, module_id, time_spent):
        """
        Record user activity in a module
        
        Args:
            module_id (str): The module identifier
            time_spent (int): Time spent in seconds
            
        Returns:
            dict: Updated progress information
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
        
        # Update time spent and last activity
        progress.time_spent += time_spent
        progress.last_activity = datetime.utcnow()
        
        # If no quiz taken yet, update completion percentage based on time
        # Assuming average module takes 10 minutes (600 seconds) to complete
        if progress.quiz_score is None:
            target_time = 600  # seconds
            time_based_completion = min(100.0, (progress.time_spent / target_time) * 100)
            progress.completion_percentage = max(progress.completion_percentage, time_based_completion)
        
        db.session.commit()
        
        return {
            'module_id': module_id,
            'time_spent_total': progress.time_spent,
            'completion_percentage': progress.completion_percentage,
            'last_activity': progress.last_activity.isoformat()
        }
    
    def get_progress_summary(self):
        """
        Get summary of user's progress across all modules
        
        Returns:
            dict: Summary of user progress
        """
        # Get all progress records for user
        progress_records = Progress.query.filter_by(user_id=self.user_id).all()
        
        # Calculate overall statistics
        total_modules = len(progress_records)
        completed_modules = sum(1 for p in progress_records if p.completion_percentage >= 100.0)
        
        total_time_spent = sum(p.time_spent for p in progress_records)
        avg_completion = sum(p.completion_percentage for p in progress_records) / total_modules if total_modules > 0 else 0
        
        # Get recently active modules
        recent_cutoff = datetime.utcnow() - timedelta(days=7)
        recent_modules = [
            {
                'module_id': p.module_id,
                'last_activity': p.last_activity.isoformat(),
                'completion_percentage': p.completion_percentage
            }
            for p in progress_records
            if p.last_activity >= recent_cutoff
        ]
        
        # Get modules that need attention (incomplete and not recently active)
        attention_modules = [
            {
                'module_id': p.module_id,
                'completion_percentage': p.completion_percentage,
                'last_activity': p.last_activity.isoformat()
            }
            for p in progress_records
            if p.completion_percentage < 100.0 and p.last_activity < recent_cutoff
        ]
        
        return {
            'total_modules': total_modules,
            'completed_modules': completed_modules,
            'completion_rate': completed_modules / total_modules if total_modules > 0 else 0,
            'total_time_spent': total_time_spent,
            'average_completion': avg_completion,
            'recent_modules': recent_modules,
            'needs_attention': attention_modules
        }
    
    def get_module_progress(self, module_id):
        """
        Get detailed progress for a specific module
        
        Args:
            module_id (str): The module identifier
            
        Returns:
            dict: Detailed module progress
        """
        progress = Progress.query.filter_by(
            user_id=self.user_id,
            module_id=module_id
        ).first()
        
        if not progress:
            return {
                'module_id': module_id,
                'status': 'not_started',
                'completion_percentage': 0.0,
                'time_spent': 0,
                'quiz_taken': False
            }
        
        # Determine status based on completion percentage
        status = 'not_started'
        if progress.completion_percentage >= 100.0:
            status = 'completed'
        elif progress.completion_percentage > 0:
            status = 'in_progress'
        
        return {
            'module_id': module_id,
            'status': status,
            'completion_percentage': progress.completion_percentage,
            'time_spent': progress.time_spent,
            'last_activity': progress.last_activity.isoformat(),
            'quiz_taken': progress.quiz_score is not None,
            'quiz_score': progress.quiz_score,
            'quiz_time_taken': progress.quiz_time_taken,
            'emotional_state': progress.emotional_state
        }
    
    def get_learning_recommendations(self):
        """
        Generate personalized learning recommendations
        
        Returns:
            list: Recommended modules and content
        """
        # Get all progress records
        progress_records = Progress.query.filter_by(user_id=self.user_id).all()
        
        recommendations = []
        
        # If user has no progress yet, recommend starting modules
        if not progress_records:
            recommendations.append({
                'type': 'module',
                'id': 'module_1',
                'reason': 'recommended_starting_point'
            })
            return recommendations
        
        # Check for incomplete modules
        incomplete_modules = [p for p in progress_records if p.completion_percentage < 100.0]
        if incomplete_modules:
            # Sort by completion percentage (highest first) to recommend most nearly complete modules first
            incomplete_modules.sort(key=lambda p: p.completion_percentage, reverse=True)
            for module in incomplete_modules[:3]:  # Recommend up to 3 incomplete modules
                recommendations.append({
                    'type': 'module',
                    'id': module.module_id,
                    'completion_percentage': module.completion_percentage,
                    'reason': 'continue_progress'
                })
        
        # Check for modules with low quiz scores that might need review
        low_score_modules = [
            p for p in progress_records 
            if p.quiz_score is not None and p.quiz_score < 70.0 and p.completion_percentage >= 100.0
        ]
        if low_score_modules:
            # Sort by quiz score (lowest first) to prioritize modules with lowest scores
            low_score_modules.sort(key=lambda p: p.quiz_score)
            for module in low_score_modules[:2]:  # Recommend up to 2 modules to review
                recommendations.append({
                    'type': 'review',
                    'id': module.module_id,
                    'quiz_score': module.quiz_score,
                    'reason': 'review_material'
                })
        
        # Check for next logical module in sequence
        completed_modules = [p.module_id for p in progress_records if p.completion_percentage >= 100.0]
        if completed_modules:
            # Simplified approach - assuming modules are named like "module_1", "module_2", etc.
            import re
            module_numbers = []
            for module_id in completed_modules:
                match = re.match(r'module_(\d+)', module_id)
                if match:
                    module_numbers.append(int(match.group(1)))
            
            if module_numbers:
                next_module_num = max(module_numbers) + 1
                next_module_id = f'module_{next_module_num}'
                
                # Check if this next module is already in recommendations
                if not any(r['id'] == next_module_id for r in recommendations):
                    recommendations.append({
                        'type': 'module',
                        'id': next_module_id,
                        'reason': 'next_in_sequence'
                    })
        
        return recommendations
   
    # backend/ai_backend/adaptive_learning/user_progress.py

# Add these optimized methods to your UserProgressTracker class

    def get_optimized_progress_summary(self):
        """
        Get summary of user's progress across all modules with optimized queries
        
        Returns:
            dict: Summary of user progress
        """
        try:
            # Use a single query with aggregate functions
            from sqlalchemy import func
            
            # Get total modules and completion stats in one query
            stats = db.session.query(
                func.count().label('total_modules'),
                func.sum(
                    func.case(
                        [(Progress.completion_percentage >= 100.0, 1)], 
                        else_=0
                    )
                ).label('completed_modules'),
                func.sum(Progress.time_spent).label('total_time_spent'),
                func.avg(Progress.completion_percentage).label('avg_completion')
            ).filter_by(user_id=self.user_id).first()
            
            # Get recent modules - use limit to avoid large result sets
            recent_cutoff = datetime.utcnow() - timedelta(days=7)
            recent_modules = Progress.query.filter_by(user_id=self.user_id).filter(
                Progress.last_activity >= recent_cutoff
            ).order_by(Progress.last_activity.desc()).limit(10).all()
            
            recent_module_data = [
                {
                    'module_id': p.module_id,
                    'last_activity': p.last_activity.isoformat(),
                    'completion_percentage': p.completion_percentage
                }
                for p in recent_modules
            ]
            
            # Get modules needing attention - with efficient filters
            attention_modules = Progress.query.filter_by(user_id=self.user_id).filter(
                Progress.completion_percentage < 100.0,
                Progress.last_activity < recent_cutoff
            ).order_by(Progress.completion_percentage.asc()).limit(5).all()
            
            attention_module_data = [
                {
                    'module_id': p.module_id,
                    'completion_percentage': p.completion_percentage,
                    'last_activity': p.last_activity.isoformat()
                }
                for p in attention_modules
            ]
            
            # Calculate completion rate safely
            completion_rate = (
                stats.completed_modules / stats.total_modules 
                if stats.total_modules > 0 else 0
            )
            
            return {
                'total_modules': stats.total_modules,
                'completed_modules': stats.completed_modules,
                'completion_rate': completion_rate,
                'total_time_spent': stats.total_time_spent,
                'average_completion': stats.avg_completion or 0,
                'recent_modules': recent_module_data,
                'needs_attention': attention_module_data
            }
        except Exception as e:
            print(f"Error generating optimized progress summary: {e}")
            # Fall back to standard method if optimization fails
            return self.get_progress_summary()