from django.urls import path

from .views import IndexView, ApiCreateView

app_name = 'displayconf'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/create/', ApiCreateView.as_view(), name='create-api'),
]
