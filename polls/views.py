from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Choice, Question

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:4]
	context = {
		'latest_question_list': latest_question_list,
	}
	return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	#response = "You are looking at the result of question %s."
	#return HttpResponse(response % question_id)
	return HttpResponse("You are looking at the result of question %s." % question_id)

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
