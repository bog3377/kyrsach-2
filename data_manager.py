from datetime import datetime

def format_exam_data(exams):
    """Convert exam data to pandas DataFrame with formatted dates"""
    if not exams:
        return pd.DataFrame()
    
    df = pd.DataFrame(exams)
    df['end_time'] = df.apply(
        lambda x: x['datetime'] + pd.Timedelta(hours=x['duration']),
        axis=1
    )
    return df

def get_exam_conflicts(exam, existing_exams):
    """Check for conflicts with existing exams"""
    conflicts = []
    exam_start = exam['datetime']
    exam_end = exam_start + pd.Timedelta(hours=exam['duration'])
    
    for existing in existing_exams:
        existing_start = existing['datetime']
        existing_end = existing_start + pd.Timedelta(hours=existing['duration'])
        
        if (exam_start < existing_end and exam_end > existing_start):
            if (exam['room'] == existing['room'] or
                exam['examiner'] == existing['examiner'] or
                exam['group'] == existing['group']):
                conflicts.append(existing)
    
    return conflicts
