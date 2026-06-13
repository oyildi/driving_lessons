from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
import os
import re

def get_dt(text):
    month_names = ["january" ,"febuary" , "march" , "april" , "may" , "june" , "july" , "august" , "september" , "october" , "november" , "december"]
    match = re.search(r'(\d{1,2})/(\d{1,2})', text)

    if match:
        m = int(match.group(1))
        d = int(match.group(2))
    else:
        
        m = None
        d = None
        for i, month in enumerate(month_names, start=1):
            match2 = re.search(
                rf'{month}\s+(\d{{1,2}})(?:st|nd|rd|th)',
                text
            )
            if match2:
                m = i
                d = int(match2.group(1))
                break

    
    dt = dict(month =m, day = d,time =None)
    return dt

def event_check(service, times , lesson_date):
    hours = []
    for t in times:
        m = re.search(r'(\d{1,2})', t)
        if m:
            hours.append(int(m.group(1)))
    print(hours)
    for hour in sorted(hours, reverse=True):

        military_hour = hour

        if hour != 12:
            military_hour += 12

        lesson_start = datetime(
            lesson_date.year,
            lesson_date.month,
            lesson_date.day,
            military_hour,
            0,
            tzinfo=ZoneInfo("America/New_York")
        )

        # 30 min drive before
        protected_start = lesson_start - timedelta(minutes=30)

        # 1 hr lesson + 30 min drive home
        protected_end = lesson_start + timedelta(hours=1, minutes=30)
        print(protected_start.isoformat())
        print(protected_end.isoformat())

        body = {
                "timeMin": protected_start.isoformat(),
                "timeMax": protected_end.isoformat(),
                "items": [{"id": "primary"}]
            }
        print(body)

        result = service.freebusy().query(
            body=body
        ).execute()

        busy = result["calendars"]["primary"]["busy"]

        if len(busy) == 0:
            return hour
    print("Unavailable")
    return None
