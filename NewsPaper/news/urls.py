from django.urls import path
from .views import PostList, PostDetail, CategoriesList, CategoriesFilter, PostSearch, NewsCreate, NewsEdit, PostDelete,\
   subscribe, mailing  # create_news
# from .views import IndexView


urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detal'),
   path('categories/', CategoriesList.as_view(), name='categories_list'),
   path('categories/<int:pk>', CategoriesFilter.as_view(), name='categories_filter'),
   path('search/', PostSearch.as_view(), name='search'),
   path('create/', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('subscribe/<int:pk>', subscribe, name='subscribe'),
   #   path('mailing/', mailing, name='mailing'),
   #   path('create/', create_news, name='create_news'),
]
