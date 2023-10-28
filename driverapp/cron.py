
from driverapp.models import Document
from datetime import datetime

def my_scheduled_job():
  pass

def document_scheduled_job_check():
    today=datetime.today().strftime("%Y-%m-%d")
    print('today',today)
    qs=Document.objects.filter(expired=False)
    for doc in qs:
        exp=doc.expiration_date.strftime("%Y-%m-%d")
        if exp>=today:
            doc.expired=True
            doc.save()
            
