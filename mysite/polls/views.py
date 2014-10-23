# from django.shortcuts import render # versions 1 and 5
from django.shortcuts import get_object_or_404, render # version 7 includes get_object_or_404

# from django.http import HttpResponse, Http404 # added HttpResponse for version 1 and Http404 for version 6
# from django.http import HttpResponse # added HttpResponse for version 1 and Http404 for version 6 # removed Http404 for version 7

# from django.http import HttpResponseRedirect, HttpResponse # version 8 adds HttpResponseRedirect
from django.core.urlresolvers import reverse
from polls.models import Choice, Question

# Create your views here.

# version 9:
from django.http import HttpResponseRedirect # version 9 removes HttpResponse
from django.views import generic

# version 10:
from django.utils import timezone

# edited as per https://docs.djangoproject.com/en/1.7/intro/tutorial03/

my_site = "Robin Gowin's sample polls site"
# version 11: exclude future questions from detail vies
my_version = 11

# debugging
def myprint(mystr1, mystr2):
	print "%s: %s version %d:%s" % (mystr1, my_site, my_version, mystr2)

# version 1
def oldindex(request):
	# return HttpResponse("Hello, world. You're at the polls index.") # version 1
	return HttpResponse("Hello, world. You're at the polls index for %s." % my_site) # version 1b

def results_v1(request, question_id):
	response = "You're looking at the results of question %s in %s."
	return HttpResponse(response % (question_id, my_site))

def results_v8(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	myprint("results", str(question))

	return render(request, 'polls/results.html', {'question': question})

def vote_v1(request, question_id):
	return HttpResponse("You're voting on question %s in %s." % (question_id, my_site))

# version 8, unchanged in version 9
def vote(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		myprint("vote", str(p))
		return render(request, 'polls/detail.html', { 'question': p, 'error_message': "You didn't select a choice.", })
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Always return an HttpResponseRedirect after successfully dealing
		# with POST data. This prevents data from being posted twice if a
		# user hits the Back button.
		myprint("vote", str(p))
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

# version 2

def detail_v2(request, question_id):
	return HttpResponse("You're looking at question %s in %s." % (question_id, my_site))

# version 6
def detail_v6(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		from django.http import Http404 # Http404 for version 6
		raise Http404

	myprint("in detail, question is", str(question))

	return render(request, 'polls/detail.html', {'question': question})

# version 7
def detail_v8(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	myprint("in detail, question is", str(question))
	return render(request, 'polls/detail.html', {'question': question})

# version 3

from polls.models import Question

def index_v4(request):
	# query the db for the 5 most recent questions
	latest_question_list = Question.objects.order_by('-pub_date')[:5]

	# output = my_site + ': ' + ', '.join([p.question_text for p in latest_question_list]) # added site name # version 3
	# print "output is: %s" % output # optional debug - goes to the console from python manage.py runserver # version 3
	# return HttpResponse(output) # version 3

	# version 4
	from django.template import RequestContext, loader # added for version 4
	template = loader.get_template('polls/index.html')
	context = RequestContext(request, { 'latest_question_list': latest_question_list, })

	print "context is: %s" % my_site + ':' + str(context)

	return HttpResponse(template.render(context))

# version 5
def index_v8(request):
	latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
	context = {'latest_question_list': latest_question_list}
	myprint("context is", str(context))

	return render(request, 'polls/index.html', context)

# Leave the rest of the views (detail, results, vote) unchanged

# version 9
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""
		Return the last five published questions (not including those set to be
		published in the future).
		"""
		# version 1: """Return the last five published questions."""
		# version 1: # return Question.objects.order_by('-pub_date')[:5]
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	# version 11
	def get_queryset(self):
		"""
		Excludes any questions that aren't published yet.
		"""
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

