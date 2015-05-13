from django.conf.urls import patterns, include, url

urlpatterns = patterns('testcasemgmt.views',
    (r'^$', 'home'),
    (r'^load_category/$', 'load_category'),
    (r'^load_testcases/$', 'load_testcases'),
    (r'^add/$', 'add_testcase'),
    (r'^import/$', 'import_testcases'),
    (r'^edit/$', 'edit_testcase'),
    (r'^delete/$', 'delete_testcase'),
    
)