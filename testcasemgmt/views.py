from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from testcasemgmt.models import TestCase
from projectmgmt.models import Project
from projectmgmt.models import Category
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.context_processors import csrf
from testcasemgmt.helper import Helper


tc = TestCase()

@login_required
def home(request):
    c = {}
    c.update(csrf(request))
    projects = Project.objects.all()
    c['projects'] = projects
    return render_to_response('testcase_home.html',
                              c, context_instance=RequestContext(request))

def load_category(request):
    if request.method == "POST":
        pid = request.POST['p_name']
    else:
        pid = ""
    q = Project.objects.get(id=pid)
    categories = q.category_set.all()
    return render_to_response('load_category.html',
                              {'categories' : categories })
    
def load_testcases(request):
    if request.method == "POST":
        pid = request.POST['p_name']
        cid = request.POST['c_name']
    
    testcases = tc.filter(pid, by="category", cid=cid) 
    
    return render_to_response('testcase_list.html',
                              {'testcases' : testcases })
    
def add_testcase(request):
    message = ""
    if request.method == "POST":
        project = Project.objects.get(id=request.POST['project'])
        category= project.category_set.get(id=request.POST['category'])
        title = request.POST['title']
        steps = request.POST['steps']
        expected_result = request.POST['expected_result']
        test_case = TestCase(project=project,category=category,
                             title=title, steps=steps, created_by=request.user,
                             expected_result=expected_result)
        try:
            test_case.save()
            message = "Testcase has been added successfully"
        except:
            import sys
            print sys.exc_info()
            message = "Failed to add testcase"
        
    c = {}
    c.update(csrf(request))
    projects = Project.objects.all()
    c['projects'] = projects
    c['message'] = message
    return render_to_response('add_testcase.html',
                              c, context_instance=RequestContext(request))

def import_testcases(request):
    failure_count = 0
    if request.method == "POST":
        cid = request.POST['category']
        pid = request.POST['project']
        project = Project.objects.get(id=pid)
        category = project.category_set.get(id=cid)
        helper = Helper()
        data = helper.parse_xls(request.FILES)
        print data
        for tc in data:
            #print tc
            test_case = TestCase(project=project,category=category,
                             created_by=request.user,
                             title=tc['title'], steps=tc['steps'],
                             expected_result=tc['expected_result']
                             )
            try:
                test_case.save()
            except:
                failure_count += 1
                continue
        
    c = {}
    c.update(csrf(request))
    projects = Project.objects.all()
    c['projects'] = projects
    c['failure_count'] = failure_count
    return render_to_response('import_testcases.html',
                              c, context_instance=RequestContext(request))
    
def delete_testcase(request):
    pass

def edit_testcase(request):
    pass


