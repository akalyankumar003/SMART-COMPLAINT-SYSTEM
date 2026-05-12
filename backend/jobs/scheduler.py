from apscheduler.schedulers.background import BackgroundScheduler
from extensions import mongo
from datetime import datetime, timedelta

def process_pending_reports():
    """Mock background job to process reports"""
    print(f"[{datetime.utcnow()}] Running background job: Processing pending reports...")
    # Example logic: auto-assign complaints
    # complaints = mongo.db.complaints.find({'status': 'Pending'})
    # ...

def initialize_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=process_pending_reports, trigger="interval", minutes=60)
    scheduler.start()
    
    # Shut down the scheduler when exiting the app
    import atexit
    atexit.register(lambda: scheduler.shutdown())
