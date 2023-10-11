from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from django.shortcuts import render
from .forms import PostForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import datetime
from django.core.cache import cache  # импортируем наш кэш


class PostList(ListView):
    model = Post
    ordering = '-datetime'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10


class CategoriesList(ListView):
    model = Category
    ordering = 'name'
    template_name = 'categories.html'
    context_object_name = 'categories'


class CategoriesFilter(ListView):
    model = Post
    ordering = '-datetime'
    template_name = 'categories_filter.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(category__pk=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_pk = self.kwargs.get('pk')
        category = Category.objects.all()[category_pk - 1]
        context['category_name'] = category.name
        context['category_pk'] = category_pk
        context['username'] = self.request.user.username
        context['is_not_subscriber'] = not category.subscribers.filter(username=self.request.user).exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'

    # --- Кэш ---
    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта, как ни странно

        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        # кэш очень похож на словарь, и метод get действует так же.
        # Он забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
            print(f'Пост pk={self.kwargs["pk"]} загружен из БД.')
        else:
            print(f'Пост pk={self.kwargs["pk"]} загружен из кэша.')

        return obj


class PostSearch(ListView):
    model = Post
    ordering = '-datetime'
    template_name = 'search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

# Альтернативный способ

# def create_news(request):
#     form = PostForm()
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         form.select = Post.news
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/news/')
#     return render(request, 'news_edit.html', {'form': form})


class NewsCreate(PermissionRequiredMixin, CreateView):

    permission_required = ('news.add_post', )

    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def form_valid(self, form):

        post = form.save(commit=False)

        if 'news' in self.request.path:
            select = Post.news
        elif 'articles' in self.request.path:
            select = Post.article

        post.select = select

        # вызовем заранее предка, чтобы достать оттуда url
        http = super().form_valid(form)

        # создаём список e-mail для рассылки...
        categories = self.request.POST.getlist('category')

        subscribers = []
        for i in categories:
            category = Category.objects.all()[int(i)-1]
            for j in category.subscribers.all():
                if j.email != '' and j.email not in subscribers:
                    subscribers.append(j.email)
        # print('Список email:', subscribers)

        # получаем наш html
        html_content = render_to_string(
            'post_created.html',
            {
                'title': self.request.POST.get('title'),
                'text': self.request.POST.get('text'),
                'link': settings.SITE_URL + http.url,
            }
        )

        # создаём рассылку
        msg = EmailMultiAlternatives(
            subject=self.request.POST.get('title'),
            body='',
            from_email='pythontestuser@yandex.ru',
            to=subscribers,
        )
        msg.attach_alternative(html_content, "text/html") # добавляем html
        msg.send() # отсылаем

        return http


class NewsEdit(PermissionRequiredMixin, UpdateView):

    permission_required = ('news.change_post', )

    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

    def get_form(self):
        form = super(UpdateView, self).get_form()
        if self.object.select != Post.news:
            self.template_name = 'message.html'
            return None
        return form


class PostDelete(PermissionRequiredMixin, DeleteView):

    permission_required = ('news.delete_post',)

    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')


class ArticleEdit(PermissionRequiredMixin, UpdateView):

    permission_required = ('news.change_post', )

    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'

    def get_form(self):
        form = super(UpdateView, self).get_form()
        if self.object.select != Post.article:
            self.template_name = 'message.html'
            return None
        return form


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if user.username == '':  # защита от взлома
        return render(request, 'subscribe.html', {'category': category, 'message': 'Чтобы подписаться, необходимо войти.'})
    category.subscribers.add(user)
    return render(request, 'subscribe.html', {'category': category, 'message': 'Подписка оформлена!'})



def mailing(request, **kwargs):
    # здесь я тестил рассылку
    return render(request, 'mailing.html', {'message': 'Рассылка выполнена!'})
