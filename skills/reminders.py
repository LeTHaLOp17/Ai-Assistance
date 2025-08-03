from apscheduler.schedulers.background import BackgroundScheduler
import time
from tts import speak

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_reminder(message, time_str):
    # For demo, interpret 'in 5 seconds', 'at 18:00', etc.
    # This requires a time parsing library for production; here's a basic fixed example:
    import datetime
    if "in " in time_str:
        seconds = int(time_str.replace("in ", "").replace(" seconds", ""))
        run_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
    else:
        # "at HH:MM" (24h)
        run_time = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(time_str, "%H:%M").time())
    scheduler.add_job(lambda: speak(f"REMINDER: {message}"), "date", run_date=run_time)
