from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView, RedirectView
from rest_framework import viewsets
from rest_framework.parsers import JSONParser

from .models import API
from .serializers import ApiSerializer


def handler(request, api):
    if request.method == 'GET':
        serializer = ApiSerializer(api)
        return JsonResponse(serializer.data, status=200)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ApiSerializer(api, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=404)

    elif request.method == 'DELETE':
        api.delete()
        return HttpResponse(status=204)


@csrf_exempt
def get_info(request, name):
    try:
        api = API.objects.filter(name=name)
        print(api[0])
    except API.DoesNotExist:
        return HttpResponse(status=404)

    return handler(request, api[0])


@csrf_exempt
def get_data(request, pk):
    try:
        api = API.objects.build_target(pk=pk)
        print(api)
    except API.DoesNotExist:
        return HttpResponse(status=404)

    return handler(request, api)


class ApiViewSet(viewsets.ModelViewSet):
    queryset = API.objects.all()
    serializer_class = ApiSerializer


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
