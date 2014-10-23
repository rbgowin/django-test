
# test1:
'''
from polls.models import Question, Choice   # Import the model classes we just wrote.
from django.utils import timezone
q = Question(question_text="What's new?", pub_date=timezone.now())
q.save()
q.id
Question.objects.all()
'''

# test2:

from polls.models import Question, Choice

# Make sure our __str__() addition worked.
Question.objects.all()
# [<Question: What's up?>]

# Django provides a rich database lookup API that's entirely driven by
# keyword arguments.
Question.objects.filter(id=1)
# [<Question: What's up?>]
Question.objects.filter(question_text__startswith='What')
# [<Question: What's up?>]

# Get the question that was published this year.
from django.utils import timezone
current_year = timezone.now().year
Question.objects.get(pub_date__year=current_year)
# <Question: What's up?>

# Request an ID that doesn't exist, this will raise an exception.
Question.objects.get(id=2)
# Traceback (most recent call last):
#   ...
# DoesNotExist: Question matching query does not exist.

# Lookup by a primary key is the most common case, so Django provides a
# shortcut for primary-key exact lookups.
# The following is identical to Question.objects.get(id=1).
Question.objects.get(pk=1)
# <Question: What's up?>

# Make sure our custom method worked.
q = Question.objects.get(pk=1)
q.was_published_recently()
# True

# Give the Question a couple of Choices. The create call constructs a new
# Choice object, does the INSERT statement, adds the choice to the set
# of available choices and returns the new Choice object. Django creates
# a set to hold the "other side" of a ForeignKey relation
# (e.g. a question's choice) which can be accessed via the API.
q = Question.objects.get(pk=1)

# Display any choices from the related object set -- none so far.
q.choice_set.all()
# []

# Create three choices.
q.choice_set.create(choice_text='Not much', votes=0)
# <Choice: Not much>
q.choice_set.create(choice_text='The sky', votes=0)
# <Choice: The sky>
c = q.choice_set.create(choice_text='Just hacking again', votes=0)

# Choice objects have API access to their related Question objects.
c.question
# <Question: What's up?>

# And vice versa: Question objects get access to Choice objects.
q.choice_set.all()
# [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]
q.choice_set.count()
# 3

# The API automatically follows relationships as far as you need.
# Use double underscores to separate relationships.
# This works as many levels deep as you want; there's no limit.
# Find all Choices for any question whose pub_date is in this year
# (reusing the 'current_year' variable we created above).
Choice.objects.filter(question__pub_date__year=current_year)
# [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]

# Let's delete one of the choices. Use delete() for that.
c = q.choice_set.filter(choice_text__startswith='Just hacking')
c.delete()

python -c "
import sys
sys.path = sys.path[1:]
import django
print(django.__path__)"

# test 'future' publish date
import datetime
from django.utils import timezone
from polls.models import Question
# create a Question instance with pub_date 30 days in the future
future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))
# was it published recently?
future_question.was_published_recently()
# True


from django.test.utils import setup_test_environment
setup_test_environment()

from django.test import Client
# create an instance of the client for our use
client = Client()

# get a response from '/'
response = client.get('/')
# we should expect a 404 from that address
response.status_code
# 404
# on the other hand we should expect to find something at '/polls/'
# we'll use 'reverse()' rather than a hardcoded URL
from django.core.urlresolvers import reverse
response = client.get(reverse('polls:index'))
response.status_code
# 200
response.content
# '\n\n\n    <p>No polls are available.</p>\n\n'
# note - you might get unexpected results if your ``TIME_ZONE``
# in ``settings.py`` is not correct. If you need to change it,
# you will also need to restart your shell session
from polls.models import Question
from django.utils import timezone
# create a Question and save it
q = Question(question_text="Who is your favorite Beatle?", pub_date=timezone.now())
q.save()
# check the response once again
response = client.get('/polls/')
response.content
# '\n\n\n    <ul>\n    \n        <li><a href="/polls/1/">Who is your favorite Beatle?</a></li>\n    \n    </ul>\n\n'
# If the following doesn't work, you probably omitted the call to
# setup_test_environment() described above
response.context['latest_question_list']
# [<Question: Who is your favorite Beatle?>]
