from django.conf.urls import patterns, include, url
import executionmgmt.views as exec_views



urlpatterns = patterns('',
   
    url(r'^$', exec_views.index),
    url(r'^get/(?P<tp_id>\d+)/$', exec_views.get_execution_detail),
    url(r'^start/$', exec_views.start_execution),
    #url(r'^(?P<p_id>\d+)/category/add/$', exec_views.add_category),
    url(r'^execute/(?P<tp_id>\d+)/tc/(?P<eh_id>\d+)/$', exec_views.execute),
    
    url(r'^get/(?P<tp_id>\d+)/filter/$', exec_views.filtered_data),
    url(r'^get/(?P<tp_id>\d+)/allocate/$', exec_views.allocate_task),
    url(r'^get/(?P<tp_id>\d+)/task/(?P<et_id>\d+)/$', exec_views.get_task_detail),
    url(r'^get/(?P<tp_id>\d+)/task/(?P<et_id>\d+)/testcase/$', exec_views.task_testcases),
    url(r'^get/(?P<tp_id>\d+)/task/(?P<et_id>\d+)/execute.psp$', exec_views.execute_tc),
    url(r'^get/(?P<tp_id>\d+)/task/(?P<et_id>\d+)/comment.psp$', exec_views.add_comment),
    
    url(r'^executionhistory/$', exec_views.get_execution_history),
    url(r'^testplan_status/$', exec_views.get_testplan_status),
    
    url(r'^exporttohtml/$', exec_views.report_view),
    
)