from gmail_code import send_email , calendar_service
from x_monitor import get_latest_tweet, load_last_seen, save_last_seen
from calendar_check import get_dt , event_check
from datetime import date
import os
import re

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
        # print("NEW POST DETECTED:")
        # print(text)

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
            if None in dt:
                print("Aborting")
                return
        
            #passes checks
            body = f"Hey, can I please claim the {dt['time']}pm lesson "
            if(date.today() != date_obj):
                body += f"on {day_name}"
            
            else:
                body += "today"
            send_email(
                "orhanhariyildiz@gmail.com",
                f"{dt['time']}pm claim Needham",
                body
            )
            
        else:
            pass
        
        save_last_seen(latest_id)
    else:
        print("No new post")


import time

while True:
    try:
        run()
    except Exception as e:
        print(e)

    time.sleep(45)