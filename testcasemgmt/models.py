# Testcase Models.
from django.db import models as django_models
from projectmgmt import models as project_models
from django.contrib.auth.models import User 
# Testcase Models.

class TestCase(django_models.Model):
    project = django_models.ForeignKey(project_models.Project)
    category = django_models.ForeignKey(project_models.Category)
    title = django_models.CharField(max_length=200)
    steps = django_models.TextField()
    expected_result = django_models.TextField()
    creation_date = django_models.DateTimeField('Date Created',auto_now_add=True)
    created_by = django_models.ForeignKey(User)
    is_automated = django_models.BooleanField(default=False)
    status = django_models.CharField(max_length=10, default='NE')
    
    def __unicode__(self):
        return self.title
    
    def filter(self, pid, **kwargs):
        project = project_models.Project.objects.get(id=pid)
        
        by = kwargs.get('by','all')
        title = kwargs.get('title','')
        
        if by == "all":
            testcases = project.testcase_set.all()
        elif by == "category":
            cid = kwargs.get('cid','')
            if title == "":
                category = project.category_set.get(id=cid)
                testcases = category.testcase_set.all()
            else:
                category = project.category_set.get(id=cid)
                testcases = category.testcase_set.filter(title)
        else:
            testcases = project.testcase_set.filter(title)
        return testcases
            

class TestcaseHistory(django_models.Model):
    testcase = django_models.ForeignKey(TestCase)
    project = django_models.ForeignKey(project_models.Project)
    title = django_models.CharField(max_length=200)
    steps = django_models.TextField()
    expected_result = django_models.TextField()
    is_automated = django_models.BooleanField()
    modified_date = django_models.DateTimeField('Date Modified',auto_now_add=True)
    modified_by = django_models.ForeignKey(User)