from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Post, Category
from django.shortcuts import render, reverse, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

# ===================================================
# Отправку новостей на почту сделал через views.py
# Дело в том, что тут медлено обновляются данные, и категории не успевают обновиться при вызове процедуры
# ===================================================

# @receiver(m2m_changed, sender=Post.category)
# def notify_post_created(sender, instance, created, **kwargs):
#     if created:
#         print('sending e-mail...')
#         print(instance.title)
#         pk = instance.pk
#         post = Post.objects.get(pk=pk)
#         print(post)
#         print(post.category.all())

        # categories = instance.category.all()
        # print(categories)
        #
        # subscribers = []
        # for category in categories:
        #     print(category)
        #     print(category.subscribers.all())
        #     subscribers += category.subscribers.all()
        #
        # print(subscribers)

        # получаем наш html
        # html_content = render_to_string(
        #     'post_created.html',
        #     {
        #         'post': instance,
        #         'link': f'{settings.SITE_URL}/news/{instance.pk}',
        #         'username': 'username'
        #     }
        # )
        #
        # msg = EmailMultiAlternatives(
        #     subject=instance.title,
        #     body=instance.text,
        #     from_email='pythontestuser@yandex.ru',
        #     to=['den1101@mail.ru'],
        # )
        # msg.attach_alternative(html_content, "text/html")  # добавляем html
        # msg.send()  # отсылаем

        # return redirect('create/')
