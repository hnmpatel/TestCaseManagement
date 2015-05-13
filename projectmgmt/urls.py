from django.conf.urls import patterns, include, url
import projectmgmt.views as proj_views



urlpatterns = patterns('',
   
    url(r'^$', proj_views.index),
    url(r'^get/(?P<p_id>\d+)/$', proj_views.get_project_detail),
    url(r'^add/$', proj_views.add_project),
    url(r'^(?P<p_id>\d+)/category/add/$', proj_views.add_category),
    
    url(r'^getProjectCategory.psp$', proj_views.get_project_category),
    url(r'^getBuildDetails.psp$', proj_views.get_build_details),
    url(r'^getBuilds.psp$', proj_views.get_builds),
    url(r'^(?P<p_id>\d+)/builds/add/$', proj_views.add_build),
    
   
)