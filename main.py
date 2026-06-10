from gmail_code import send_email , calendar_service
from x_monitor import get_latest_tweet, load_last_seen, save_last_seen
from calendar_check import get_dt , event_check
from datetime import date , datetime, timezone, timedelta
from zoneinfo import ZoneInfo
import os
import time
import re

tz = ZoneInfo("America/New_York")

def has_needham(text):
    return "needham" in text

def unclaimed(text):
    return "claimed" not in text

def run():
    tweet = get_latest_tweet()
    service = calendar_service()

    latest_id = tweet["id"]
    text = tweet["text"]
    text_lower = text.lower()

    last_seen = load_last_seen()

    if latest_id != last_seen:
        print("NEW POST DETECTED")
        try:
            created = datetime.fromisoformat(
                tweet["created_at"].replace("Z", "+00:00")
            )

            seen = datetime.now(timezone.utc)

            print(f"created: {created.isoformat()}")
            print(f"seen:    {seen.isoformat()}")
            print(f"delay:   {(seen - created).total_seconds():.3f} seconds")
        except Exception as er:
            print(f"Failed to retrieve creation stats due to: '{er}' , straight to parsing")

        #parse

        if(has_needham(text=text_lower) and unclaimed(text=text_lower)):   
            dt = get_dt(text=text_lower)
            date_obj = date(2026, dt['month'], dt['day'])
            day_name = date_obj.strftime("%A")
            lessons = text_lower.splitlines()
            times = []
            for lesson in lessons:
                if("needham" in lesson and "email" not in lesson):
                    needham_times = re.findall(
                        r'\b\d{1,2}(?:-\d{1,2})?\s*pm\b',
                        lesson
                    )
                    times.extend(needham_times)
                
            
            dt['time'] = event_check(
                service=service, times=times, lesson_date=date_obj
            )
            if dt["time"] is None:
                print("Aborting")
                save_last_seen(latest_id)
                return

        
            #passes checks
            body = f"Hey, can I please claim the {dt['time']}PM lesson "
            if(date.today() != date_obj):
                body += f"on {day_name}"
            
            else:
                body += "today"
            body += "\n\nBest,\nOrhan Yildiz"
            if "none" in body.lower():
                print("Aborting")
                save_last_seen(latest_id)
                return

            send_email(
                "info@needhamdrivingschool.com",
                f"{dt['time']}PM claim Needham",
                body
            )
            
        else:
            pass
        save_last_seen(latest_id)

    else:
        print("No new post")


while True:
    try:
        now = datetime.now(tz)

        if 6 <= now.hour <= 21:
            run()
        
        time.sleep(3)
    except Exception as e:
        print(f"Error: {e}")

   