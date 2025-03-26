from datetime import datetime, timedelta

def validate_exam(new_exam, existing_exams):
    """
    Validate new exam entry for conflicts
    Returns True if no conflicts, False otherwise
    """
    new_start = new_exam['datetime']
    new_end = new_start + timedelta(hours=new_exam['duration'])
    
    for exam in existing_exams:
        exam_start = exam['datetime']
        exam_end = exam_start + timedelta(hours=exam['duration'])
        
        # Check for time overlap
        if new_start < exam_end and new_end > exam_start:
            # Check for resource conflicts
            if (new_exam['room'] == exam['room'] or
                new_exam['examiner'] == exam['examiner'] or
                new_exam['group'] == exam['group']):
                return False
    
    return True
