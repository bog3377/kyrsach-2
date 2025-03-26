from datetime import datetime, timedelta

def show_calendar(exams):
    if not exams:
        return "Нет данных для отображения"

    return format_calendar_data(exams)

def format_calendar_data(exams):
    calendar_data = []
    for exam in exams:
        event = {
            'title': f"{exam['group']} ({exam['room']})",
            'start': exam['datetime'],
            'end': exam['datetime'] + timedelta(hours=exam['duration']),
            'examiner': exam['examiner']
        }
        calendar_data.append(event)

    return calendar_data