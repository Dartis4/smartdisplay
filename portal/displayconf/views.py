from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView

from .forms import NameEntryForm, APIForm
from .models import API


def index(request):
    api_list = API.objects.all()
    context = {'api_list': api_list}
    return render(request, 'pages/index.html', context)


def create_api(request):
    if request.method == "POST":
        form = NameEntryForm(request.POST)
        if form.is_valid():
            print("API name:", form.cleaned_data['name'])
            new_api = form.save()
            return HttpResponseRedirect(reverse('displayconf:enter_api', args=(new_api.id,)))
    else:
        form = NameEntryForm()
    return render(request, 'create_api.html', {'form': form})


def enter_api(request):
    if request.method == "POST":
        form = APIForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('displayconf:index'))
    else:
        form = APIForm()
    return render(request, 'enter_api.html', {'form': form})
