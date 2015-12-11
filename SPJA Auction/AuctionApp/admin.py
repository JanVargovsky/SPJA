from django.contrib import admin

#from .models import CustomUser
from .models import Item, TaskStatus, Task

#admin.site.register(CustomUser)
admin.site.register(Item)
admin.site.register(TaskStatus)
admin.site.register(Task)