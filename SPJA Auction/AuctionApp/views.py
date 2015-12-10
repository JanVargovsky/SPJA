from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.models import User

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home'
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
            'showEdit': username is None or (username is not None and  User.objects.get_by_natural_key(username) is request.user),
            'customuser': request.user if username is None else User.objects.get_by_natural_key(username),
        }))

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