from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "tasks"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('<int:task_id>/book', views.book, name="book"),
    path('<int:task_id>/revoke', views.revoke, name="revoke"),
    path('<int:task_id>/download', views.download, name="download"),
    path('<int:task_id>/delete/', views.delete, name="delete"),
    path('new/', views.new_task, name="new_task"),
    path('new/success', views.new_task_success, name="new_task_success"),
] 