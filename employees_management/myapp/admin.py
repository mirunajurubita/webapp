# Register your models here.
from django.contrib import admin
from .models import User, Managers, Employee, Tasks

# Register your models here.
admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Tasks)

admin.site.register(Managers)



