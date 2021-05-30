import textwrap

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Ключ для создания URL',
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/', null=True, blank=True
    )

    def __str__(self):
        formatted_text = textwrap.shorten(self.text, 20)
        return (
            'Запись: '
            f'Автор: {self.author}, '
            f'Сообщество: {self.group}, '
            f'Дата публикации: {self.pub_date.date()}, '
            f'Текст: {formatted_text}'
        )

    class Meta:
        ordering = ('-pub_date',)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('-created',)


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers',
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following',
    )

    class Meta():
        unique_together = ['user', 'following', ]
