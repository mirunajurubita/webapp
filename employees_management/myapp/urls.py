from django.urls import path, include
from . import views 
from . import apiviews
from myapp import ManagerViews, EmployeeViews
from knox import views as knox_views
from rest_framework.authtoken import views as views_aut
from myapp.apiviews import  LoginAPI, RegisterAPI
from knox import views as knox_views
from rest_framework.authtoken.views import obtain_auth_token

#from .apiviews import 
urlpatterns = [
    path('', views.index, name = 'index'),
    path('loginUser', views.loginUser, name = 'loginUser'),
    #path('loginPage', views.loginPage, name = 'loginPage'),
    path('registerEmployee', EmployeeViews.EmployeeSignUpView.as_view(), name='registerEmployee'),
    path('registerAdmin', ManagerViews.ManagerSignUpView.as_view(), name='registerAdmin'),    
    path('logoutUser', views.logoutUser, name = 'logoutUser'),
    path('managerPage', ManagerViews.manager_page, name = 'managerPage'),
    path('employeePage', EmployeeViews.employee_page, name = 'employeePage'),
    path("addTask", ManagerViews.addTask, name = "addTask"),
    path("addTaskSave", ManagerViews.addTaskSave, name = "addTaskSave"),
    path("viewAllEmployees", ManagerViews.viewAllEmployees, name = "viewAllEmployees"),
    path("viewAllTeammates", EmployeeViews.viewAllTeammates, name = "viewAllTeammates"),
    path("viewClosedTasks", ManagerViews.viewClosedTasks, name = "viewClosedTasks"),
    path("viewActiveTasks", EmployeeViews.viewActiveTasks, name = "viewActiveTasks"),
    path("viewAllTasks", ManagerViews.viewAllTasks, name = "viewAllTasks"),
    path('endTask/<int:id>', EmployeeViews.endTask, name='endTask'),
    #path('addTaskSave/<int:deadline>', ManagerViews.addTaskSave, name='addTaskSave'),
    path("employeeClosedTasks", EmployeeViews.employeeClosedTasks, name = "viewClosedTasks"),
    path("particularEmployee/<str:username>", ManagerViews.particularEmployee, name = "particularEmployee"),
    path("viewActivity/<str:username>", ManagerViews.viewActivity, name = "viewActivity"),
    #path('api/user/', apiviews.userViewSet.as_view() , name = "user"),
    #path('api/employee', apiviews.employeeViewSet.as_view() , name = "employee"),
    #path('api/task/', apiviews.taskViewSet.as_view() , name = "task"),

    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/registerser/', RegisterAPI.as_view(), name='login'),

    path('api/seeActiveTasks/', apiviews.seeActiveTasks, name='logoutall'),
    path('api-token-auth', obtain_auth_token, name='api-token-auth'),


]
