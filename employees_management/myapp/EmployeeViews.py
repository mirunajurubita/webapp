from pyexpat.errors import messages
from time import time
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from urllib3 import HTTPResponse
from .models import Employee, Managers, User, Tasks
from .forms import EmployeeSignUpForm
from django.views.generic import CreateView
from django.db.models import F
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils import timezone
import datetime 
import numpy as np

#@login_required()
def employee_page(request):
    return render(request, "employee_page.html")
    
class EmployeeSignUpView(CreateView):
    model = User
    form_class = EmployeeSignUpForm
    template_name = 'register_employee.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'employee'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('loginUser')

def viewAllTeammates(request): 
    tasks = Employee.objects.all()
    employees = User.objects.filter(is_employee=1)
    return render(request, 'view_all_teammates.html',{'employees': employees,'tasks':tasks})

#@login_required()
def viewActiveTasks(request):
    current_user = request.user
    current_user_id = current_user.id
    employees = Employee.objects.filter(user_id = current_user_id)
    user_employees = User.objects.filter(is_employee=1)
    tasks = Tasks.objects.filter()
    return render(request, "employees_active_tasks.html", {'employees':employees,'user_employees':user_employees,'tasks':tasks})

def endTask(request, id):
    #user_employees = User.objects.filter(is_employee=1)
    employees=Employee.objects.get(user_id=request.user.id)
    task = Tasks.objects.get(id=id, employee_id = employees.id)
    user_employees = User.objects.filter(is_employee=1, id = employees.user_id)

    #labelid = request.GET.get["id"]
    #task = Tasks.objects.get(id = labelid)

    #Tasks.objects.filter(id = id).update(is_active=0)
    task.is_active = 0
    task.closed_at = timezone.now()
    employees.completed_tasks = employees.completed_tasks +1
    employees.active_tasks = employees.active_tasks -1 
    """
    if task.closed_at.day > task.deadline.day and task.closed_at.month > task.deadline.month:
        task.is_overdue = 1
    elif task.closed_at.day > task.deadline.day:
        task.is_overdue = 1
    elif task.closed_at.hour > task.deadline.hour and task.closed_at.minute > task.deadline.minute:
        task.is_overdue = 1
    elif task.closed_at.minute > task.deadline.minute:
        task.is_overdue = 1
    """
    if task.closed_at < task.assigned_at:
        task.is_oveordue=1
        
    if task.is_overdue == 0: 
        diff = task.closed_at - task.assigned_at
    else:
        diff = task.assigned_at - task.closed_at

    if task.deadline.year == task.assigned_at.year and  task.deadline.month == task.assigned_at.month and task.deadline.day == task.assigned_at.day:
        task.days = diff.days
        task.seconds = diff.seconds
        task.hours = task.days * 24 + task.seconds // 3600
        task.minutes = (task.seconds % 3600) // 60
        task.seconds = task.seconds % 60
    elif task.closed_at.year == task.assigned_at.year and  task.closed_at.month == task.assigned_at.month and task.closed_at.day == task.assigned_at.day:
        task.days = diff.days
        task.seconds = diff.seconds
        task.hours = task.days * 24 + task.seconds // 3600
        task.minutes = (task.seconds % 3600) // 60
        task.seconds = task.seconds % 60
    else:
        if task.deadline.day - task.assigned_at.day == 1:
            
            time_of_work = diff.total_seconds() / 3600.00 - 16.00
            task.days = 0
            task.hours = int(time_of_work)
            task.minutes = int((time_of_work - task.hours) * 60)
            task.seconds = int(((time_of_work - task.hours) * 60 - task.minutes)*60)

        elif task.deadline.day - task.assigned_at.day > 1:
            closed_at_date = task.closed_at.date()
            assigned_at_date = task.assigned_at.date()
            total_days = task.closed_at.day - task.assigned_at.day +1
            weekend_days = np.busday_count(assigned_at_date, closed_at_date, weekmask='0000011')
            time_of_work = (diff.total_seconds() / 3600.00) - 16 - 24*weekend_days
            #- 16*(total_days - 2)
            task.days = int(time_of_work/16)
            task.hours = int(time_of_work-int(time_of_work/16)*16)
            task.minutes = int((time_of_work-int(time_of_work/16)*16 - task.hours) * 60)
            task.seconds = int(((time_of_work-int(time_of_work/16)*16 - task.hours) *60 - task.minutes)*60)
  
    employees.save()
    task.save()
    return render(request, "employees_end_tasks.html", {"employees": employees,"task":  task,  "user_employees":  user_employees})
    #return render(request, "employees_eactive_tasks.html")

#return render(request, 'employees_end_tasks.html')

def employeeClosedTasks(request):
    employees = Employee.objects.all()
    user_employee = request.user
    tasks = Tasks.objects.all().order_by('-closed_at')
    return render(request, 'employee_closed_tasks.html',{"employees": employees,"tasks":tasks,"user_employee": user_employee})




