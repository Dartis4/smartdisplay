from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, RedirectView

from .models import API


def info(request, api_id):
    api = get_object_or_404(API, pk=api_id)
    return HttpResponseRedirect(reverse('displayconf:results', args=(api.id,)))


class SubmitRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'api-detail'


class GenericDetailView(DetailView):
    model = API
    template_name = 'pages/detail.html'


class IndexView(ListView):
    template_name = 'pages/index.html'
    context_object_name = 'latest_api_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_api_list'] = API.objects.all()[:5]
        return context

    def get_queryset(self):
        return API.objects.order_by('-creation_date')[:5]


class ResultView(DetailView):
    model = API
    template_name = 'pages/result.html'


class ApiCreateView(CreateView):
    template_name = 'forms/enter_api_info.html'
    model = API
    fields = '__all__'


class ApiUpdateView(UpdateView):
    template_name = 'forms/enter_api_info.html'
    model = API
    fields = '__all__'


class ApiDeleteView(DeleteView):
    # template_name = 'forms/enter_api_info.html'
    model = API
    success_url = reverse_lazy('api-list')
