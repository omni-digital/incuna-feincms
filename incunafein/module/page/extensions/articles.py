"""
Add a many-to-many relationship field to relate this page to articles.Article.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page

def register(cls, admin_cls):
    cls.add_to_class('articles', models.ManyToManyField('articles.Article', blank=True,
        #related_name='%(app_label)s_%(class)s_related',
        null=True, help_text=_('Select articles that should be listed as related content.')))

    try:
        admin_cls.filter_horizontal.append('articles')
    except AttributeError:
        admin_cls.filter_horizontal = ['articles']

    admin_cls.fieldsets.append((_('Articles'), {
        'fields': ('articles',),
        'classes': ('collapse',),
        }))

