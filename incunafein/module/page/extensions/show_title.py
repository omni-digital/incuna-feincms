from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms import extensions

"""
Add a show_title flag to the page
"""


class Extension(extensions.Extension):
    def handle_model(self):
        self.model.add_to_class(
            'show_title',
            models.BooleanField(_('show title'), default=True),
        )

    def handle_modeladmin(self, modeladmin):
        modeladmin.add_extension_options(_('Show title'), {
            'fields': ('show_title',),
            'classes': ('collapse',),
        })
