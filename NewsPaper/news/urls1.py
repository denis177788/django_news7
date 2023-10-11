from django.urls import path
from .views import PostDelete, NewsCreate, ArticleEdit

urlpatterns = [
   path('create/', NewsCreate.as_view(), name='article_create'),
   path('<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
