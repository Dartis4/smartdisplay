from django.urls import path

from . import views
from .views import IndexView, ApiCreateView, ResultView

app_name = 'displayconf'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', ApiCreateView.as_view(), name='create-api'),
    path('<int:pk>/result/', ResultView.as_view(), name='results'),
    # path('<int:api_id>/get/', views.get_info, name='get-info')
]
