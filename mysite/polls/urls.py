# from https://docs.djangoproject.com/en/1.7/intro/tutorial03/

from django.conf.urls import patterns, url

from polls import views

# urlpatterns_v0 = patterns( '', url(r'^$', views.index, name='index'),)

# version 1
'''
# need to comment out because it peeks inside url()
urlpatterns_v1 = patterns('',
	# ex: /polls/
	url(r'^$', views.index, name='index'), # here $ at end of regex is ok
	# ex: /polls/5/
	url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'), # here $ at end of regex is ok
	# ex: /polls/5/results/
	url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'), # here $ at end of regex is ok
	# ex: /polls/5/vote/
	url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'), # here $ at end of regex is ok
)
'''

# version 2 - try to get more generic
urlpatterns = patterns('',
	url(r'^$', views.IndexView.as_view(), name='index'),
	url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
	url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
	url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),

)

