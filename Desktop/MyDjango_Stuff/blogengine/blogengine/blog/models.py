from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time

def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))

# Create your models here.
class Post (models.Model):
    title = models.CharField(max_length= 150, db_index=True)
    slug = models.SlugField(max_length= 150, blank = True, unique=True)
    body = models.TextField(blank = True, db_index = True)
    tags = models.ManyToManyField('Tag', blank = True, related_name = 'posts')
    img = models.ImageField(blank = True, upload_to='images/', default='images/default.png',)
    date_pub =  models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_pub']

class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
# В файлі tag_list є посилання Для нього і була створеня ф-я нижче
# {% for tag in post.tags.all %}
# <a href="{{ tag.get_absolute_url }}">{{ tag.title }}</a>
# {% endfor %}
    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']

class Site(models.Model):
    client = models.CharField(max_length=50)
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique=True)

    def get_absolute_url(self):
        return reverse('site_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('site_update_url', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('site_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)

    class Meta:
        ordering = ['title']
