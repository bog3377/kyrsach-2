from datetime import datetime, timedelta

def format_datetime(dt):
    """Format datetime for display"""
    return dt.strftime("%d.%m.%Y %H:%M")

def parse_datetime(date_str, time_str):
    """Parse date and time strings to datetime object"""
    try:
        return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError:
        return None

def calculate_end_time(start_time, duration):
    """Calculate end time based on start time and duration"""
    return start_time + timedelta(hours=duration)

def get_date_range(exams):
    """Get the date range for all exams"""
    if not exams:
        return None, None
    
    dates = [exam['datetime'] for exam in exams]
    return min(dates), max(dates)
