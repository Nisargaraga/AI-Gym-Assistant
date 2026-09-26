class PoseService:
    @staticmethod
    def calculate_session_scores(exercise: str, reps: int, duration_minutes: int) -> dict:
        """
        Calculate metrics for a single workout session.
        Returns a dictionary with performance_score, form_score, consistency_score, and endurance_score.
        """
        # Form Score: Real-world bicep curl or squat form can be evaluated.
        # We simulate a high form score (85-95) with some natural variance based on rep count.
        # If reps are too low or too high, form tends to fatigue.
        if reps == 0:
            form = 0.0
        elif reps < 5:
            form = 82.0
        elif reps < 15:
            form = 92.5
        elif reps < 30:
            form = 89.0
        else:
            form = 84.5  # fatigue sets in
        # Endurance Score: based on duration vs standard targets (e.g., 20 mins is a good target)
        if duration_minutes == 0:
            endurance = 0.0
        else:
            # 20 minutes active workout is 100% endurance
            endurance = min(100.0, (duration_minutes / 20.0) * 100.0)
            
        # Consistency Score: we default to a standard session score of 85,
        # which will be aggregated by the analytics service over multiple sessions.
        consistency = 85.0
        
        # Overall Performance: weighted average
        if reps == 0 or duration_minutes == 0:
            perf = 0.0
        else:
            perf = round((form * 0.5) + (endurance * 0.3) + (consistency * 0.2), 1)
        return {
            "performance_score": perf,
            "form_score": round(form, 1),
            "consistency_score": round(consistency, 1),
            "endurance_score": round(endurance, 1)
        }
