from celery import shared_task
# from time import sleep
from blog.models import Task

# @shared_task
# def sendEmail():
#     sleep(3)
#     print("Done sending email!")
    

@shared_task
def delete_completed_tasks():
    deleted_count, _ = Task.objects.filter(completed=True).delete()
    return f"{deleted_count} completed tasks deleted."