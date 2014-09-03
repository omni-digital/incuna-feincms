"""
Add a allow_comments flag to the page
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms import extensions


class Extension(extensions.Extension):
    def handle_model(self):
        self.model.add_to_class(
            'allow_comments',
            models.BooleanField(_('allow comments'), default=False,),
        )

    def handle_modeladmin(self, modeladmin):
        modeladmin.extend_list('list_filter', ['allow_comments'])
        modeladmin.add_extension_options(_('Allow comments'), {
            'fields': ('allow_comments',),
            'classes': ('collapse',),
        })
