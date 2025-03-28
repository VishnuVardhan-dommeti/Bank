import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


from celery.schedules import crontab

app.conf.beat_schedule = {
    'calculate-interest-daily': {
        'task': 'Custom_admin.tasks.calculate_interest',
        'schedule': crontab(hour=0, minute=0),  # Midnight
    },
    'mark-dormant-weekly': {
        'task': 'Custom_admin.tasks.mark_dormant_accounts',
        'schedule': crontab(day_of_week=0, hour=1, minute=0),  # Every Sunday at 1 AM
    },
    'monthly-summaries': {
        'task': 'Custom_admin.tasks.generate_monthly_summaries',
        'schedule': crontab(day_of_month=1, hour=2, minute=0),  # 1st of every month
    }
}
