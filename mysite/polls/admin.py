from django.contrib import admin

# Register your models here.

# edited per https://docs.djangoproject.com/en/1.7/intro/tutorial02/

from polls.models import Question, Choice # version 2 add Choice

# register the Question (polls site)

# initial version, takes all defaults:
# admin.site.register(Question)

# newer version: change sequence of fields displayed

# version 3
# class ChoiceInline(admin.StackedInline): # first version
class ChoiceInline(admin.TabularInline): # second version
	model = Choice
	extra = 3


class QuestionAdmin(admin.ModelAdmin):
	# fields = ['pub_date', 'question_text'] # first version
	fieldsets = [
		(None,               {'fields': ['question_text']}),
		# ('Date information', {'fields': ['pub_date']}), # first version
		('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}), # collapse this field by default
	]
	inlines = [ChoiceInline]
	list_display = ('question_text', 'pub_date', 'was_published_recently') # version 4; gives more detail on the "Select question to change" page

	# version 4: add a filter
	list_filter = ['pub_date']

	# version 5: add search
	search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice) # version 2 # comment out for version 3

