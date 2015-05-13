from django.conf.urls import patterns, include, url
from testcasemgmt import urls as testcase_urls

from django.contrib import admin
admin.autodiscover()
handler404 = 'tcms.views.pagenotfound'
handler403 = 'tcms.views.notauthorized'

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^testcase/', include(testcase_urls)),
    (r'^$', 'tcms.views.index'),
	(r'^home/', 'tcms.views.home'),
    (r'^login/$','tcms.views.login'),
    (r'^auth/$','tcms.views.auth_view'),
    (r'^logout/$','tcms.views.logout'),
    (r'^invalid/$','tcms.views.invalid_login'),

    url(r'^project/', include('projectmgmt.urls')),
    url(r'^execution/', include('executionmgmt.urls')),
)
