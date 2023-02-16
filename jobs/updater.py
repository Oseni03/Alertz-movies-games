from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from jobs.date_updater import Updater


def start():
    print("At start")
    scheduler = BackgroundScheduler()
    task = Updater()
    scheduler.add_job(task.main, "interval", minutes=5)
    scheduler.start()
    print("Here")
