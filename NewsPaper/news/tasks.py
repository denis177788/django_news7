from celery import shared_task
from .models import Post, Category
import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

@shared_task
def mailing():
    print('Рассылка...')
    for category in Category.objects.all():
        print('-----------------')
        print(category.name)
        subscribers = []
        for j in category.subscribers.all():
            if j.email != '' and j.email not in subscribers:
                subscribers.append(j.email)
        print(subscribers)

        date = datetime.datetime.today()
        week = date.strftime("%V")
        posts = Post.objects.filter(datetime__week=week, category=category.pk).order_by('-datetime')
        print(posts.values('title', 'datetime'))
        print(len(posts))

        if (len(posts) > 0) and (len(subscribers) > 0):
            print('>0')

            # получаем наш html
            html_content = render_to_string(
                'mailing_form.html',
                {
                    'category_name': category.name,
                    'posts': posts
                }
            )

            # создаём рассылку
            msg = EmailMultiAlternatives(
                subject=f'Свежие новости от News Portal! Категория: {category.name}',
                body='',
                from_email='pythontestuser@yandex.ru',
                to=subscribers,
            )

            # добавляем html
            msg.attach_alternative(html_content, "text/html")

            # отсылаем
            try:
                msg.send()
                print(f'Рассылка по категории {category.name} успешно выполнена!')
            except:
                print(f'Неудачная попытка почтовой рассылки по категории {category.name}!')

