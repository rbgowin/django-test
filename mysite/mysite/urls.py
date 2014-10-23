from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'mysite.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	# url(r'^polls/', include('polls.urls')), # explicitly avoid $ at end of regex # version 1 with no namespace
	url(r'^polls/', include('polls.urls', namespace="polls")), # version 2 with namespace
	url(r'^admin/', include(admin.site.urls)), # added # explicitly avoid $ at end of regex
)


# edited as per https://docs.djangoproject.com/en/1.7/intro/tutorial03/

