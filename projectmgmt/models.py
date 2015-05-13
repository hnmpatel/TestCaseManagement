from django.db import models


# Project Models.

class Project(models.Model):
    name = models.CharField(max_length=200)
    description =  models.TextField()
    is_active = models.BooleanField(default = True)
    
    def __unicode__(self):
        return self.name
    

class Category(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=200)
    description =  models.TextField()
    is_active = models.BooleanField()
    
    def __unicode__(self):
        return self.name
    
class Build(models.Model):
    project = models.ForeignKey(Project)
    version = models.CharField(max_length=200)
    description =  models.TextField()
    
    def __unicode__(self):
        return self.version
    
    
       
    
class ClientDevice(models.Model):
    project = models.ForeignKey(Project)
    client_device = models.CharField(max_length=200)
    operating_system = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.client_device
    
class Browser(models.Model):
    browser = models.CharField(max_length=200)
    
