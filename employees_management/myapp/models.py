#from django.contrib.auth.models import AbstractUser
from django.db import models
from tkinter import CASCADE
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



# Create your models here.




class User(AbstractUser):
    is_admin= models.BooleanField('Admin', default=False)
    is_employee = models.BooleanField('Employee', default=False)

class Managers(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = models.Manager()
    #def __str__(self):
    #    return self.user.username 



class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    objects = models.Manager()
    address=models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    #number_of_completed_tasks = models.IntegerField(default = 0)
    active_tasks = models.IntegerField(default = 0)
    completed_tasks = models.IntegerField(default = 0)

    #def __str__(self):
    #   return self.user.username   

class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee,blank=True,null=True,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default = 1)
    is_active = models.IntegerField(default = 1)
    is_overdue = models.IntegerField(default = 0)
    headline = models.CharField(max_length = 100)
    body = models.TextField()
    assigned_at =models.DateTimeField(auto_now_add = True)
    dflt = timezone.now()
    closed_at =  models.DateTimeField(default = dflt)
    deadline = models.DateTimeField(default = dflt)
    hours = models.IntegerField(default = 0)
    minutes = models.IntegerField(default = 0)
    days = models.IntegerField(default = 0)
    seconds = models.IntegerField(default = 0)
    hours = models.IntegerField(default = 0)

    #objects = models.Manager()
"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__is_active = self.active

    def save(self, *args, **kwargs):
        if not self.is_active and self.__is_active:
            self.closed_at = datetime.now()
        super().save(*args, **kwargs)
"""

"""

@receiver(post_save, sender = CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type ==1:
            Manager.objects.create(admin=instance)
        if instance.user_type ==2:
            Employee.objects.create(admin=instance, tasks_id = Tasks.objects.get(id=1),daily_r ="",weekly_r="",monthly_r="",annual_r="")

@receiver(post_save, sender = CustomUser)
def save_user_profile(sender, instance,  **kwargs):
    if instance.user_type ==1:
        instance.manager.save()
    if instance.user_type ==2:
        instance.employee.save()
"""


