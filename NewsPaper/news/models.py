from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} (рейтинг: {self.rating})'

    # Метод update_rating() модели Author, который обновляет рейтинг текущего автора (метод принимает в качестве аргумента только self).
    # Он состоит из следующего:
    #     суммарный рейтинг каждой статьи автора умножается на 3;
    #     суммарный рейтинг всех комментариев автора;
    #     суммарный рейтинг всех комментариев к статьям автора.
    def update_rating(self):
        new_rating = 0
        # статьи
        q1 = Post.objects.filter(author_id=self.pk).values('rating')
        for i in range(0, len(q1)):
            new_rating += (q1[i]['rating'] * 3)
        # комментарии
        q2 = Comment.objects.filter(user_id=self.user).values('rating')
        for i in range(0, len(q2)):
            new_rating += q2[i]['rating']
        # комментарии к статьям
        q3 = Comment.objects.filter(post__author__user=self.user).values('rating')
        for i in range(0, len(q3)):
            new_rating += q3[i]['rating']
        # пишем
        self.rating = new_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User)  # related_name='categories'

    def __str__(self):
        return self.name

class Post(models.Model):

    news = 'N'
    article = 'A'
    POSITIONS = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    select = models.CharField(max_length=1, choices=POSITIONS, default=news)
    datetime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    category = models.ManyToManyField(Category)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.datetime} {self.title} {self.text} (Автор: {self.author.user})'

    def get_absolute_url(self):
        return reverse('post_detal', args=[str(self.id)])

    # при обновлении данных, необходимо удалить их из кэша:
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123]+'...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.text


# class Mailing(models.Model):
#     datetime = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.datetime



