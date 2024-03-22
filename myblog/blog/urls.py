from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('list/', views.list_post, name='list'),
    path('list/<slug:tag_slug>', views.list_post, name='list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.detail_post, name="post_detail"),
    path('create/', views.create_post, name='post_create'),
    path('<int:pk>/delete/', views.delete_post, name='delete'),
    path('<int:pk>/update/', views.update_post, name='update'),
    path('about/', views.about_me,name='about'),
    
    

]
