from __future__ import division
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from models import TestPlan, ExecutionHistory, ExecutionTask
from projectmgmt.models import Project, Category, Build, Browser, ClientDevice
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from testcasemgmt.models import TestCase, TestcaseHistory
from django.template import RequestContext
import time
from testcasemgmt.models import TestCase

from django.http.response import HttpResponse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt



import datetime

import json
import commands


# Create your views here.
def index(request):
    testplans = TestPlan.objects.all()
    dict_obj = []
    for testplan in testplans:
        #print get_testplan_status(testplan.id)
        dict_obj.append({'testplan':testplan, 'status':get_testplan_status(testplan.id)})
    
    
    return render_to_response('executions_home.html', {'testplans' : testplans, 'dict_obj': dict_obj,'active':'active'}, context_instance=RequestContext(request))
    
def start_execution(request):
    args = {}
    args.update(csrf(request))
    
    projects = Project.objects.all()
    args['projects'] = projects
    args['active'] = 'active'
    
    if request.POST:
        
        title = request.POST['title']
        build = Build.objects.get(id=request.POST['build'])
        project = Project.objects.get(id=request.POST['project'])
        description = request.POST['description']
        
        test_plan = TestPlan(project = project, title = title, build = build , description = description, started_by = request.user)
        test_plan.save()
            
        return HttpResponseRedirect("/execution/")
        
    else:
        return render_to_response('start_execution.html', args)


def get_execution_detail(request, tp_id):
    testplan = TestPlan.objects.get(id = tp_id)
    execution_tasks = testplan.executiontask_set.all()
    #categories =  execution.executionhistory_set.values('testcase__category__name').distinct()
    
    return render_to_response('testplan_task_list.html', {'testplan': testplan,'execution_tasks': execution_tasks, 'active':'active'}, context_instance=RequestContext(request))

def execute(request, et_id):
    args = {}
    args.update(csrf(request))
    execution_task = ExecutionTask.objects.get(id = et_id)
    
    args['execution_task'] = execution_task
    
   
    '''
    if request.POST:
        
        result = request.POST['result']
        bug_id = request.POST['bugid']
        comment = request.POST['comment']
        
        if result == 'PASS':
            execution_history.bugid = 0
            execution_history.comment = ''
            if comment !='':
                execution_history.comment = comment
       
        else:
            if bug_id != '' and comment !='':
                execution_history.bugid = bug_id
                execution_history.comment = comment
        
        execution_history.result = result
        #print request.user
        execution_history.executed_by = request.user
        execution_history.save()
        
        # Calculate execution status.
        total_tc = execution_task.executionhistory_set.count()
        passed_tc = execution_task.executionhistory_set.filter(result='PASS').count()
        failed_tc = execution_task.executionhistory_set.filter(result='FAIL').count()
        nap_tc = execution_task.executionhistory_set.filter(result='NAp').count()
        
        
        
        execution_status = ( (passed_tc + failed_tc + nap_tc)/total_tc ) * 100
        
        #print execution_status 
        
        execution_task.status = execution_status
        
        execution_task.save()
          
        return render_to_response('execution.html', args)

        
    else:
        return render_to_response('execution.html', args)
    '''
    return render_to_response('execution.html', args, context_instance=RequestContext(request))
    


def filtered_data(request, ex_id):
    execution = TestPlan.objects.get(id = ex_id)
    execution_history = None
    filter_by = None
    
    categories =  execution.executionhistory_set.values_list('testcase__category__name', flat=True).distinct()
    
    
    
    if 'by' not in request.GET:
        by = "All"
        execution_history = execution.executionhistory_set.all()
    
    
        
        
    else:
        filter_by = request.GET['by']
    
        if filter_by == 'pass':
            by = "Passed"
            execution_history = execution.executionhistory_set.filter(result='PASS')
        elif filter_by == 'fail':
            by = "Failed"
            execution_history = execution.executionhistory_set.filter(result='FAIL')
        elif filter_by == 'nap':
            by = "Not Applicable"
            execution_history = execution.executionhistory_set.filter(result='NAp')
        elif filter_by == 'ne':
            by = "Not Executed"
            execution_history = execution.executionhistory_set.filter(result='NE')
        elif filter_by == 'executed':
            by = "Executed"
            execution_history = execution.executionhistory_set.filter(result__in=['PASS','FAIL','NAp'])
        else:
            by = "All"
            execution_history = execution.executionhistory_set.all()
    args = {}      
    args['execution'] = execution
    args['execution_history'] = execution_history 
    args['categories'] = categories
    #args['categories'] = execution.executionhistory_set.all().testcase_set.all()
    
    
    
    args['filter_by'] = by
    return render_to_response('execution_filter.html', args, context_instance=RequestContext(request))

def allocate_task(request, tp_id):
    args = {}
    args.update(csrf(request))
    testplan = TestPlan.objects.get(id = tp_id)
    args['testplan'] = testplan
    args['users'] = User.objects.all()
    args['browsers'] = Browser.objects.all()
    args['client_devices'] = ClientDevice.objects.all()
    
    
    if request.POST:
        
        title = request.POST['title']
        description = request.POST['description']
        allocate_to = User.objects.get(id=request.POST['allocate_to'])
        client_device = ClientDevice.objects.get(id=request.POST['client_device'])
        browsers = request.POST.getlist('browsers')
        browser_name = ''
        for browser in browsers:
            browser_name = browser_name + ',' + browser
                              
        browser_name =  browser_name[1:]
        category = Category.objects.get(id=request.POST['category'])
        
        execution_task = ExecutionTask(testplan = testplan, title = title,
                                       description = description,
                                       allocated_to = allocate_to,
                                       allocated_by = request.user,
                                       client_device = client_device,
                                       browsers = browser_name, category=category)
        execution_task.save()
        
        
        testcases = TestCase.objects.filter(category = category)
        
        for testcase in testcases:
            execution_history =  ExecutionHistory(execution = execution_task, testcase = testcase)
            execution_history.save()
        
        return HttpResponseRedirect("/execution/get/"+str(tp_id)+"/")
        
    else:
        return render_to_response('allocate_task.html', args, context_instance=RequestContext(request))
    
def get_task_detail(request, tp_id, et_id):
    testplan = TestPlan.objects.get(id = tp_id)
    execution_task = ExecutionTask.objects.get(id = et_id)
    #categories =  execution.executionhistory_set.values('testcase__category__name').distinct()
    
    return render_to_response('task_detail.html', {'testplan': testplan,'execution_task': execution_task, 'active':'active'}, context_instance=RequestContext(request))

def task_testcases(request, tp_id, et_id):
    testplan = TestPlan.objects.get(id = tp_id)
    execution_task = ExecutionTask.objects.get(id = et_id)
    execution_history = execution_task.executionhistory_set.all()
    
    return render_to_response('task_testcases.html', {'testplan': testplan,'execution_task': execution_task, 'execution_history':execution_history, 'active':'active'}, context_instance=RequestContext(request))
    
    
@csrf_exempt
def execute_tc(request,tp_id, et_id):
    
    #execution_history = ExecutionHistory.objects.get(id=eh_id)
    #print request.POST.get('json_data')
    json_obj = json.loads(request.POST.get('json_data'))
    
    for obj in json_obj:
        
        execution_history = ExecutionHistory.objects.get(id=obj['eh_id'])
        execution_history.result = obj['eh_result']
        
        if obj['eh_result'] == 'PASS':
            execution_history.bugid = 0
            execution_history.comment = ''
        elif obj['eh_result'] == 'FAIL':
            execution_history.bugid = obj['eh_bugid']
            execution_history.comment = obj['comment']
        elif obj['eh_result'] == 'NAp':
            execution_history.comment = obj['comment']
        else:
            execution_history.comment = obj['comment']
            
        execution_history.executed_by = request.user
        execution_history.save()
        
    # Calculate execution task status.
    execution_task = ExecutionTask.objects.get(id=et_id)
        
    total_tc = execution_task.executionhistory_set.count()
    passed_tc = execution_task.passed()
    failed_tc = execution_task.failed()
    nap_tc = execution_task.nap()
     
    execution_status = ( (passed_tc + failed_tc + nap_tc)/total_tc ) * 100
      
    execution_task.status = execution_status
        
    execution_task.save()
    
    # Calculate testplan status.
    testplan = TestPlan.objects.get(id=tp_id)
    
        
    return HttpResponse("done")

@login_required
@csrf_exempt
def add_comment(request,tp_id, et_id):
    
    json_obj = json.loads(request.POST.get('json_data'))
    
    for obj in json_obj:
        
        execution_history = ExecutionHistory.objects.get(id=obj['eh_id'])
        execution_history.comment = obj['comment']
        execution_history.save()
        
        
    return HttpResponse("done")

@login_required
@csrf_exempt
def get_execution_history(request):
    
    testcase_id = request.POST.get('tc_id')
    print testcase_id
    testcase = TestCase.objects.get(id=testcase_id)
    json_obj = []
    try:
        execution_histories = ExecutionHistory.objects.filter(testcase=testcase_id, result__in=['PASS', 'FAIL', 'NAp']).order_by('-modified_date')[:5]
     
        print execution_histories.count()
        
        for execution_history in execution_histories:
            
            json_obj.append({'testplan':execution_history.execution.title,
                             'execution_task':execution_history.execution.testplan.title,
                             'result': execution_history.result,
                             'build':execution_history.execution.testplan.build.version,
                             'bugid': execution_history.bugid,
                             'comment': execution_history.comment,
                             'executed_by': execution_history.executed_by.username,
                             'last_modified_date':str(execution_history.modified_date)})
            print json_obj
            
    except Exception, err:
        print Exception, err
        pass
    
    return HttpResponse(json.dumps(json_obj, indent=4))


def get_testplan_status(tp_id):
    
    testplan = TestPlan.objects.get(id=tp_id)
    
    total_tc = 0
    
    n_ex = 0
    
    for execution_task in testplan.executiontask_set.all():
        exec_task_total = execution_task.total()
        total_tc = total_tc + exec_task_total
        
        n_ex = n_ex + execution_task.not_ex()
        
    
    execution_status = ((total_tc - n_ex) / total_tc) * 100
    
    return round(execution_status)


    
    
    
    
    
  
def report_view(request):
    testplan = TestPlan.objects.get(id=request.GET.get('tp_id'))
    execution_tasks = testplan.executiontask_set.all()
    execution_task = ExecutionTask.objects.get(id = 1)
    
    total_tc = 0;
    passed_tc = 0;
    failed_tc = 0;
    nap_tc = 0;
    ne_tc = 0;
    
    for execution_task in testplan.executiontask_set.all():
        total_tc = total_tc + execution_task.total()
        passed_tc = passed_tc + execution_task.passed()
        failed_tc = failed_tc + execution_task.failed()
        nap_tc = nap_tc + execution_task.nap()
        ne_tc = ne_tc + execution_task.not_ex()
        
    passed_per = round(((passed_tc/total_tc)*100),2)
    failed_per = round(((failed_tc/total_tc)*100),2)
    nap_per = round(((nap_tc/total_tc)*100),2)
    ne_per = round(((ne_tc/total_tc)*100),2)
    
    
    
    #categories =  execution.executionhistory_set.values('testcase__category__name').distinct()
    
    response_html = render_to_response('generated_report.html', {'testplan': testplan,'status':get_testplan_status(testplan.id),
                                       'total_tc': total_tc,
                                       'passed_tc': passed_tc,
                                       'failed_tc': failed_tc,
                                       'nap_tc': nap_tc,
                                       'ne_tc': ne_tc,
                                       'passed_per': passed_per,
                                       'failed_per': failed_per,
                                       'nap_per': nap_per,
                                       'ne_per': ne_per},
                                       context_instance=RequestContext(request))
    #with open('/tmp/response.html', 'w') as html_file:
    #    html_file.write(str(response_html))
        
    #print response_html
    
    #ret = commands.getoutput('wkhtmltopdf --enable-javascript --javascript-delay 5000 --page-size A3 /tmp/response.html /tmp/response.pdf')
    #ret = commands.getoutput('mv /tmp/response.pdf .')
    
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="response.pdf"'
    '''
    response = HttpResponse()
    response['Content-Type'] = ''
    response['X-Sendfile'] = "/static/response.pdf"
    '''
    
    
    response = response_html
    return response




    

