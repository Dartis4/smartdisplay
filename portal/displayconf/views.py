from django.views.generic import CreateView, TemplateView

from .models import API


class IndexView(TemplateView):
    template_name = 'pages/index.html'


class ApiCreateView(CreateView):
    template_name = 'forms/enter_api_info.html'
    model = API
    fields = '__all__'
