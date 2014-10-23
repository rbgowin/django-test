from django.db import models

# Create your models here.

# copied from https://docs.djangoproject.com/en/1.7/intro/tutorial01/ and then edited

import datetime
from django.utils import timezone

class Question(models.Model):
	def __unicode__(self): # __str__ on Python 3
		return self.question_text

	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')

	def was_published_recently_v1(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

	# version 3:
	def was_published_recently(self):
		now = timezone.now()
		return now - datetime.timedelta(days=1) <= self.pub_date <= now

	# version 2
	was_published_recently.admin_order_field = 'pub_date'
	was_published_recently.boolean = True
	was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
	def __unicode__(self): # __str__ on Python 3
		return self.choice_text

	question = models.ForeignKey(Question)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
