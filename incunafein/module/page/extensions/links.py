"""
Add a many-to-many relationship field to relate this page to links.Link.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms import extensions


class Extension(extensions.Extension):

    def handle_model(self):
        self.model.add_to_class(
            'links',
            models.ManyToManyField(
                'links.Link',
                blank=True,
                null=True,
                help_text=_('Select links that should be listed as related content.'),
            ),
        )

    def handle_modeladmin(self, modeladmin):
        modeladmin.extend_list('filter_horizontal', ['links'])
        modeladmin.add_extension_options(_('Links'), {
            'fields': ('links',),
            'classes': ('collapse',),
        })
