# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import redirect, render, redirect, reverse
# from django.core.urlresolvers import reverse
from .models import Users

import re

def index(request):
        # when adding log_regis to another app, this index page will not be used
        return render(request, 'log_regis/index.html')

def show(request):
    user = Users.objects.get(id=request.session['id'])
    name = user.first_name
    context = {'name':name }
    return render(request, 'log_regis/show.html', context)

def register(request):
    if request.POST:
        results = Users.objects.registrations(request.POST)

        if not results['status']:
            for error in results['errors']:
                messages.error(request, error)
            return redirect(reverse('auth:index'))
        else:
            user = Users.objects.filter(email=request.POST['email'])
            request.session['id'] = user[0].id
            return redirect(reverse('auth:show'))
    else:
        return redirect(reverse('auth:index'))
        
def login(request):
    results = Users.objects.login(request.POST)
    print "....starting login process"
    if not results['status']:
        for error in results['errors']:
            messages.error(request, error)
            return redirect(reverse('auth:index'))
    user = Users.objects.filter(email=request.POST['email'])
    request.session['id'] = user[0].id
    return redirect(reverse('auth:show'))
       