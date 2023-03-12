from django.urls import path

from . import views

app_name = 'displayconf'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_api, name='create_api'),
    path('entry/<int:api_id>/', views.enter_api, name='enter_api')
]
