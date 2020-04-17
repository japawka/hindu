from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Choice, Question
from django.views import generic

# def index(request):
# 	latest_question_list = Question.objects.order_by('-pub_date')[:4]
# 	context = {
# 		'latest_question_list': latest_question_list,
# 	}
# 	return render(request, 'polls/index.html', context)

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		return Question.objects.order_by('-pub_date')[:5]



class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

# def detail(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	context = {
# 		'question': question
# 	}
# 	return render(request, 'polls/detail.html', context)


# def results(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	context = {
# 		'question':question
# 	}
# 	return render(request, 'polls/results.html', context)




def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'question':question,
			'error_message': "Nie zagłosowałeś, głąbie.",
		})
	else:
		selected_choice.votes +=1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
