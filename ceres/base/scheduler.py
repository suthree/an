from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

jobstores = {"default": DjangoJobStore()}
# coalesce 多任务合并执行
job_defaults = {"coalesce": True, "max_instances": 3, "misfire_grace_time": 60}
executors = {
    "default": ThreadPoolExecutor(3),
    "thread": ThreadPoolExecutor(3),
    "process": ProcessPoolExecutor(8),
}
scheduler = BackgroundScheduler(
    jobstores=jobstores,
    job_defaults=job_defaults,
    executors=executors,
)
register_events(scheduler)
scheduler.start()
