from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    booked_by = models.CharField(max_length=200)
    upload_date = models.DateTimeField("uploaded on")
    deleted = models.BooleanField("Is deleted")

    def __str__(self):
        return '%s' % (self.title)

class TaskFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    zip_file = models.FileField(upload_to='documents/%Y/%m/%d')   