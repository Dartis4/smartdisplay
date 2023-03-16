from django.urls import path

from . import views
from .views import IndexView, ApiCreateView, ResultView

app_name = 'displayconf'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', ApiCreateView.as_view(), name='create-api'),
    path('<int:pk>/submission-redirect/', views.info, name='redirect'),
    path('<int:pk>/', ResultView.as_view(), name='results')
]
