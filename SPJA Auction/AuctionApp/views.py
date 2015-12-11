from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.models import User
from AuctionApp.forms import CustomUserInfoEditForm, CreateItemForm
from AuctionApp.models import Item

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
        'users.html',
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
        'userinfo.html',
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
            'items': Item.objects,
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
        # TODO: join colleciton of collection in errors to pass only plain strings to global alert handling
        dic['dangerAlerts'] = form.errors

    return render(request,
            'userinfoedit.html',
            context_instance = RequestContext(request,dic))

def createitem(request):
    """Renders create item page."""
    assert isinstance(request, HttpRequest)
     # TODO: redirect if its not current logged user
    successCreate = False
    if request.method == 'POST':
        form = CreateItemForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data;
            item = Item(user = request.user, name = data['name'], price = data['price'])
            item.save()
            item = CreateItemForm()
            successCreate = True
    else:
        form = CreateItemForm()

    return render(request,
            'createitem.html',
            context_instance = RequestContext(request,
        {
            'title': 'Create item',
            'form': form,
            'successCreate': successCreate
        }))

def edititem(request,id):
    """Renders edit item page."""
    assert isinstance(request, HttpRequest)
     # TODO: redirect if its not current logged user
    successEdit = False
    if request.method == 'POST':
        form = CreateItemForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data;
            item = Item(user = request.user, id = id, name = data['name'], price = data['price'])
            item.save()
            successEdit = True
            #todo redirect to list
    else:
        form = CreateItemForm(instance=Item.objects.get(id = id))

    return render(request,
            'edititem.html',
            context_instance = RequestContext(request,
        {
            'title': 'Create item',
            'form': form,
            'successEdit': successEdit
        }))

def deleteitem(request,id):
    """Renders edit item page."""
    assert isinstance(request, HttpRequest)
     # TODO: redirect if its not current logged user
    item = Item.objects.get(id = id)
    if item:
        item.delete()

    return HttpResponseRedirect('/useritems/')

#def contact(request):
#    """Renders the contact page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'app/contact.html',
#        context_instance = RequestContext(request,
#        {
#            'title':'Contact',
#            'message':'Your contact page.',
#            'year':datetime.now().year,
#        })
#    )

#def about(request):
#    """Renders the about page."""
#    assert isinstance(request, HttpRequest)
#    return render(
#        request,
#        'app/about.html',
#        context_instance = RequestContext(request,
#        {
#            'title':'About',
#            'message':'Your application description page.',
#            'year':datetime.now().year,
#        })
#    )