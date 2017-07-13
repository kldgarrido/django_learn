from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render_to_response
from models import Book
from forms import ContactForm
from django.http import HttpResponseRedirect
from forms import PublisherForm

# Create your views here.
def search(request):
	query = request.GET.get('q', '')
	if query:
		qset = (
		Q(title__icontains=query) |
		Q(authors__first_name__icontains=query) |
		Q(authors__last_name__icontains=query)
		)
		results = Book.objects.filter(qset).distinct()
	else:
		results = []
	return render_to_response("search.html", {
		"results": results,
		"query": query
	})

def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			topic = form.cleaned_data['topic']
			message = form.cleaned_data['message']
			sender = form.cleaned_data.get('sender', 'noreply@example.com')
			return HttpResponseRedirect('/search/')
	else:
		form = ContactForm(initial={'sender': 'user@example.com'})
	return render_to_response('contact.html', {'form': form})


def add_publisher(request):
		if request.method == 'POST':
			form = PublisherForm(request.POST)
			if form.is_valid():
				form.save()
			return HttpResponseRedirect('/add_publisher/thanks/')
		else:
			form = PublisherForm()
		return render_to_response('add_publisher.html', {'form': form})
