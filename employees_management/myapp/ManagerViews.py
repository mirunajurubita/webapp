from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from urllib3 import HTTPResponse
from .forms import ManagerSignUpForm
from .models import Employee, User, Tasks
from django.http import  HttpResponseRedirect, HttpResponse
from django.db.models import F
from django.utils import timezone

#@login_required()
def manager_page(request):
    return render(request, "manager_page.html")


class ManagerSignUpView(CreateView):
    model = User
    form_class = ManagerSignUpForm
    template_name = 'register_manager.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('loginUser')

#@login_required()
def addTask(request):
    employees =  User.objects.filter(is_employee=1)
    
    #deadline = timezone.now() , "deadline_pick": deadline
    return render(request,"add_task.html", {'employees': employees })

#@login_required()
def addTaskSave(request):
    if request.method!="POST":
        return HTTPResponse("Method Not Allowed")
    else:
        headline=request.POST.get("headline")
        body=request.POST.get("body")
        deadline = request.POST.get("deadline")
        employee_id=request.POST.get("employee")
        employee=Employee.objects.get(user_id=employee_id)  
        employee.active_tasks = employee.active_tasks +1
        employee.save()
        user = User.objects.get(id = employee.user_id)
        try:
            task_model=Tasks(headline=headline, body = body, employee_id = employee, deadline = deadline, user_id = user)
            #task_model.author = request.user
            task_model.save()
            messages.success(request, "Task added successfully!")
            return HttpResponseRedirect(reverse("addTask"))
        except:
            return HttpResponseRedirect("addTask")
    
 
#@login_required()
def viewAllEmployees(request): 
    user_now = request.user
    tasks = Employee.objects.all()
    employees = User.objects.filter(is_employee=1)
    return render(request, 'view_all_employees.html',{'employees': employees,'tasks':tasks,"user_now ":user_now })

#@login_required()
def viewAllTasks(request):
    employees = Employee.objects.all()
    tasks = Tasks.objects.all().order_by('-closed_at')
    return render(request, 'view_all_tasks.html',{"employees": employees,"tasks":tasks})

#@login_required()
def viewClosedTasks(request):
    employees = Employee.objects.all()
    user_employee =User.objects.all()
    tasks = Tasks.objects.all().order_by('-closed_at')
    return render(request, 'view_closed_tasks.html',{"employees": employees,"tasks":tasks,"user_employee": user_employee})
    
def particularEmployee (request, username):
    employees = Employee.objects.all()
    user_employee =User.objects.get(username = username)
    tasks = Tasks.objects.all().order_by('-closed_at')
    return render(request, 'view_particular_employee.html',{"employees": employees,"tasks":tasks,"user_employee": user_employee})

def viewActivity(request, username):
    user_employee =User.objects.get(username = username)
    employee = Employee.objects.get(user_id = user_employee.id)
    tasks = Tasks.objects.all().order_by('-closed_at')
    return render(request, 'view_activity.html',{"employee": employee,"tasks":tasks,"user_employee": user_employee})



