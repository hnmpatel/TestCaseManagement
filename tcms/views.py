from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from projectmgmt.models import *
from executionmgmt.models import *
from testcasemgmt.models import *
from datetime import timedelta
from django.utils import timezone



def index(request):
    c = {}
    c.update(csrf(request))
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home')
    return HttpResponseRedirect('/login')

@login_required
def home(request):
    c = {}
    c.update(csrf(request))
    
    current_user = request.user
    tasks_allocated = ExecutionTask.objects.filter(allocated_to = current_user).count()
    c['task_allocated'] = tasks_allocated
    
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    testcases_executed_last_week = ExecutionHistory.objects.filter(executed_by = current_user).filter(result__in=['PASS','FAIL','NAp']).filter(modified_date__range=[some_day_last_week, timezone.now().date()]).count()
    c['testcases_executed_last_week'] = testcases_executed_last_week
    
    testcases_passed_last_week = ExecutionHistory.objects.filter(executed_by = current_user).filter(result__in=['PASS']).filter(modified_date__range=[some_day_last_week, timezone.now().date()]).count()
    c['testcases_passed_last_week'] = testcases_passed_last_week
    
    testcases_failed_last_week = ExecutionHistory.objects.filter(executed_by = current_user).filter(result__in=['FAIL']).filter(modified_date__range=[some_day_last_week, timezone.now().date()]).count()
    c['testcases_failed_last_week'] = testcases_failed_last_week
    
    execution_tasks = ExecutionTask.objects.filter(allocated_to = current_user)
    c['execution_tasks'] = execution_tasks
    
    return render_to_response('dashboard.html',c,context_instance=RequestContext(request))
    
def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)
    
def auth_view(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/home')
    else:
        c = {}
        c.update(csrf(request))
        c['message'] = "Invalid credentials"
        return render_to_response('login.html', c)
       
    
def loggedin(request):
    return render_to_response('loggedin.html',
                              {'full_name' : request.user.username})

def invalid_login(request):
    return render_to_response('invalid_login.html')
    
def logout(request):
    auth.logout(request)
    c = {}
    c.update(csrf(request))
    c['message'] = "You have successfully logged out."
    return render_to_response('login.html', c)

def pagenotfound(request):
    return render_to_response('page_not_found.html')

def notauthorized(request):
    return render_to_response('not_authorized.html')