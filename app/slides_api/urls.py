from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('slide-data/', views.SlidesAPIView.as_view()),
]
