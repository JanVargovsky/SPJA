from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.models import User
from AuctionApp.forms import CustomUserInfoEditForm, CreateItemForm, CreateTaskStatusForm, CreateTaskForm, EditTaskForm, SendMessageForm
from AuctionApp.models import Item, TaskStatus, Task, Message

def getFieldErrors(form):
    errors = list()
    for field in form:
        for error in field.errors:
            errors.append(error)
    return errors
    return [error for field in form for error in field.errors]

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home',
            'dangerAlerts': ('some example danger',),
            'infoAlerts': ('some example info',),
            'successAlerts': ('some example success',),
            'warningAlerts': ('some example warning',),
        }))

def login(request):
    """Renders the login page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'login.html',
        context_instance = RequestContext(request,
        {
            'title':'Login'
        }))

def users(request):
    """Renders the login page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'user/users.html',
        context_instance = RequestContext(request,
        {
            'title':'List of users',
            'users': User.objects,
        }))

def register(request):
    """Renders the register page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'register.html',
        context_instance = RequestContext(request,
        {
            'title':'Register'
        }))

def userinfo(request, username):
    """Renders the user info page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'user/userinfo.html',
        context_instance = RequestContext(request,
        {
            'title':'User info',
            'showEdit': username is None or (username is not None and request.user is not None and username == request.user.username),
            'customuser': request.user if username is None else User.objects.get_by_natural_key(username),
        }))

def error(request):
    """Renders the error page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'error.html',
        context_instance = RequestContext(request,
        {
            'title':'Error'
        }))

def useritems(request):
    """Renders items of logged user page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'items.html',
        context_instance = RequestContext(request,
        {
            'title':'My items',
            'items': Item.objects.all().filter(user = request.user),
        }))

def userinfoedit(request, username):
    # TODO: redirect if its not current logged user
    assert isinstance(request, HttpRequest)

    successSave = False
    if request.method == 'POST':

        form = CustomUserInfoEditForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            successSave = True
    else:
        form = CustomUserInfoEditForm(instance=User.objects.get_by_natural_key(username))

    dic = {
            'title': 'Edit info',
            'form': form,
        }

    if successSave:
        dic['successAlerts'] = ('Edit was successful!',)
    elif form.errors:
        dic['dangerAlerts'] = getFieldErrors(form)

    return render(request,
            'user/userinfoedit.html',
            context_instance = RequestContext(request,dic))

def createitem(request):
    """Renders create item page."""
    assert isinstance(request, HttpRequest)
     # TODO: redirect if its not current logged user
    successCreate = False
    if request.method == 'POST':
        form = CreateItemForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            item = Item(user = request.user, name = data['name'], price = data['price'])
            item.save()
            item = CreateItemForm()
            successCreate = True
    else:
        form = CreateItemForm()

    dic = {
            'title': 'Create item',
            'form': form,
        }

    if successCreate:
        dic['successAlerts'] = ('Item was created!',)
    elif form.errors:
        dic['dangerAlerts'] = getFieldErrors(form)

    return render(request,
            'createitem.html',
            context_instance = RequestContext(request, dic))

def edititem(request,id):
    """Renders edit item page."""
    assert isinstance(request, HttpRequest)
     # TODO: redirect if its not current logged user
    successEdit = False
    if request.method == 'POST':
        form = CreateItemForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            item = Item(user = request.user, id = id, name = data['name'], price = data['price'])
            item.save()
            successEdit = True
    else:
        form = CreateItemForm(instance=Item.objects.get(id = id))

    dic = {
            'title': 'Edit item',
            'form': form,
        }

    if successEdit:
        dic['successAlerts'] = ('Edit was successful!',)
    elif form.errors:
        dic['dangerAlerts'] = getFieldErrors(form)

    return render(request,
            'edititem.html',
            context_instance = RequestContext(request, dic))

def deleteitem(request,id):
    """Renders edit item page."""
    assert isinstance(request, HttpRequest)
     # TODO: redirect if its not current logged user
    item = Item.objects.get(id = id)
    if item:
        item.delete()

    return HttpResponseRedirect('/useritems/')

def taskstatuscreate(request):
    """Renders create form page for task status."""
    assert isinstance(request, HttpRequest)
    successCreate = False
    invalidForm = False
    if request.method == 'POST':
        form = CreateTaskStatusForm(request.POST)

        if form.is_valid():
            form.save()
            form = CreateTaskStatusForm()
            successCreate = True
        else:
            invalidForm = True
    else:
        form = CreateTaskStatusForm()

    return render(request,
            'taskstatus/create.html',
            context_instance = RequestContext(request,
        {
            'title': 'Create new task status',
            'form': form,
            'successAlerts': ('Created!',) if successCreate else list(),
            'dangerAlerts': ('Something went wrong!',) if invalidForm else list()
        }))

def taskstatuslist(request):
    """Renders task status list page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'taskstatus/list.html',
        context_instance = RequestContext(request,
        {
            'title':'Task status list',
            'statuses': TaskStatus.objects.all(),
        }))

def taskstatusdelete(request,id):
    taskstatus = TaskStatus.objects.get(id = id)
    if taskstatus:
        taskstatus.delete()
    return taskstatuslist(request)

def taskslist(request, filter):
    """Renders tasks list page."""
    assert isinstance(request, HttpRequest)

    tasks = Task.objects.all().filter(user = request.user)
    title = 'All tasks'
    if filter is 'notdeleted':
        tasks = tasks.filter(deleted = False)
        title = 'Active tasks'
    elif filter is 'deletedonly':
        tasks = tasks.filter(deleted = True)
        title = 'Deleted tasks'

    return render(request,
        'task/list.html',
        context_instance = RequestContext(request,
        {
            'title': title,
            'showDeleteButton': filter is not 'deletedonly',
            'tasks': tasks
        }))

def taskcreate(request):
    """Renders form to create new task."""
    assert isinstance(request, HttpRequest)

    successCreate = False
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            task = Task(user = request.user, text = data['text'], status = data['status'])
            task.save()
            form = CreateTaskForm()
            successCreate = True
        else:
            invalidForm = True
    else:
        form = CreateTaskForm()

    dic = {
            'title': 'Create new task',
            'form': form,
        }

    if successCreate:
        dic['successAlerts'] = ('Created!',)
    elif form.errors:
        dic['dangerAlerts'] = getFieldErrors(form)

    return render(request,
            'task/create.html',
            context_instance = RequestContext(request, dic))

def taskedit(request, id):
    """Renders form to create new task."""
    assert isinstance(request, HttpRequest)

    successEdit = False
    if request.method == 'POST':
        form = EditTaskForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            task = Task.objects.get(id = id)
            task.text = data['text']
            task.status = data['status']
            task.deleted = data['deleted']
            task.save()
            successEdit = True
        else:
            invalidForm = True
    else:
        form = EditTaskForm(instance=Task.objects.get(id = id))

    dic = {
            'title': 'Edit task',
            'form': form,
        }

    if successEdit:
        dic['successAlerts'] = ('Edited!',)
    elif form.errors:
        dic['dangerAlerts'] = getFieldErrors(form)

    return render(request,
            'task/edit.html',
            context_instance = RequestContext(request, dic))

def taskdelete(request,id):
    """Deletes task by id."""
    assert isinstance(request, HttpRequest)

    task = Task.objects.get(id = id)
    if task:
        task.deleted = True
        task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def messagesend(request, username):
    """Renders form to send new message."""
    assert isinstance(request, HttpRequest)

    successSend = False
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        # TODO paste assignee username into label

        if form.is_valid():
            data = form.cleaned_data
            message = Message(user_from = request.user,
                              user_to = User.objects.get_by_natural_key(username),
                              text = data['text'])
            message.save()
            form = SendMessageForm(initial={'username': User.objects.get_by_natural_key(username).username})
            successSend = True
        else:
            invalidForm = True
    else:
        form = SendMessageForm(initial={'username': User.objects.get_by_natural_key(username).username})

    dic = {
            'title': 'Send new message',
            'form': form,
        }

    if successSend:
        dic['successAlerts'] = ('Sent!',)
    elif form.errors:
        dic['dangerAlerts'] = getFieldErrors(form)

    return render(request,
            'message/send.html',
            context_instance = RequestContext(request, dic))