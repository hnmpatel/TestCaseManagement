from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from models import Project,Category,Build
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied
from django.db.models import Max
from django.contrib.comments.feeds import LatestCommentFeed

import json

# Project views are here.

@login_required(login_url='/login')
def index(request):
    projects = Project.objects.filter(is_active=True)
    return render_to_response('project_home.html', {'projects' : projects, 'active':"active"})
   
@login_required(login_url='/login')
def get_project_detail(request,p_id=1):
    args = {}
    args.update(csrf(request))
    
    project = Project.objects.get(id=p_id)
    categories = project.category_set.all()
    latest_version = Build.objects.all().aggregate(Max('version'))
    latest_version = Build.objects.get(version = latest_version['version__max'])
    
    args['project'] = project
    args['categories'] = categories
    args['latest_version'] = latest_version
    
    
    return render_to_response('project_detail.html', args)

@login_required(login_url='/login')
def add_project(request):
    
    if request.user.groups.all()[0].name not in ["admin","qa_lead"]:
        raise PermissionDenied
    else:
        
        
        args = {}
        args.update(csrf(request))
        args['active'] = 'active'
        
        if request.POST:
            proj_name = request.POST['proj_name']
            proj_desc = request.POST['proj_desc']
            
            if Project.objects.filter(name = proj_name):
                args['message'] = 'Same project already exists.'
                return render_to_response('add_project.html', args)
            else:
                project = Project(name = proj_name, description = proj_desc)
                project.save()
                print project.id   
                return HttpResponseRedirect('/project/get/'+str(project.id)+'/')
            
        else:
            
            return render_to_response('add_project.html', args)

@login_required(login_url='/login')
def add_category(request, p_id):
    args = {}
    args.update(csrf(request))
    project = Project.objects.get(id=p_id)
    args['project'] = project
    args['active'] = 'active'
    
    if request.POST:
        category_name = request.POST['category']
        category_desc = request.POST['description']
        
        if project.category_set.filter(name=category_name):
            args['message'] = 'Same category already exists in this project'
            return render_to_response('add_category.html', args)
        else:
            category = Category(project = project, name = category_name, description = category_desc)
            category.save()   
            return HttpResponseRedirect('/project/get/'+str(p_id)+"/")
        
    else:
        
        return render_to_response('add_category.html', args)

def get_project_category(request):
    project_id = request.GET['proj_id']
    data = []
    if Project.objects.get(id=project_id):
        project = Project.objects.get(id=project_id)
        
        for category in project.category_set.all():
            data.append({ "id": category.id, "name": category.name })
                      
    return HttpResponse(json.dumps(data, indent=4), 
                    mimetype="application/json") 
        
        

def get_build_details(request):
    build_id = request.GET['build']
    build = Build.objects.get(id = build_id)
    
    data = {"id": build.id,"project" : build.project.name, "description": build.description}
    return HttpResponse(json.dumps(data, indent=4), mimetype="application/json") 

def get_builds(request):
    project_id = request.GET['project']
    data = []
    if Project.objects.get(id=project_id):
        project = Project.objects.get(id=project_id)
        
        for build in project.build_set.all():
            data.append({ "id": build.id, "version": build.version })
                      
    return HttpResponse(json.dumps(data, indent=4), 
                    mimetype="application/json") 
    

def add_build(request, p_id):
    project = Project.objects.get(id=p_id)
    if request.POST:
        version = request.POST['version']
        description = request.POST['description']
        
        new_build = Build(version=version, description=description, project = project)
        
        new_build.save()
        return HttpResponseRedirect('/project/get/'+str(project.id)+'/')
        
    else:
        
        raise PermissionDenied
    
    
