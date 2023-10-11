from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):



   date = DateFilter(
       field_name='datetime',
       widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
       lookup_expr='gt',
       label='Start Date'
   )

   class Meta:
       model = Post
       fields = {
           # поиск по названию
           'title': ['icontains'],
           # по имени автора
           'author__user': ['exact'],
           # позже указываемой даты
           # 'datetime': ['date__gt'],
       }