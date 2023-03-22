from django.urls import path

from . import views
from .views import IndexView, ApiCreateView, ResultView, ApiViewSet

app_name = 'displayconf'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/', ApiCreateView.as_view(), name='create-api'),
    path('<int:pk>/result/', ResultView.as_view(), name='results'),
    path('api/get/', ApiViewSet.as_view({'get':'list'}), name='get'),
    path('api/get/<int:pk>/', views.get_data, name='get-data'),
    path('api/get/<str:name>/', views.get_info, name='get-info')
]
