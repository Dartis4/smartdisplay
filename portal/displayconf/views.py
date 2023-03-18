from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, RedirectView

from .models import API


class SubmitRedirectView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'results'


class IndexView(ListView):
    template_name = 'pages/index.html'
    context_object_name = 'latest_api_list'

    def get_queryset(self):
        return API.objects.order_by('-creation_date')[:5]


class ResultView(DetailView):
    model = API
    template_name = 'pages/result.html'

    def get_object(self, **kwargs):
        return get_object_or_404(API, pk=self.kwargs.get('pk'))


class ApiCreateView(CreateView):
    template_name = 'forms/enter_api_info.html'
    model = API
    context_object_name = 'latest_api_list'
    fields = '__all__'


class ApiUpdateView(UpdateView):
    template_name = 'forms/enter_api_info.html'
    model = API
    fields = '__all__'


class ApiDeleteView(DeleteView):
    # template_name = 'forms/enter_api_info.html'
    model = API
    success_url = reverse_lazy('api-list')
