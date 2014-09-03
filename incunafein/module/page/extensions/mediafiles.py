"""
Add a many-to-many relationship field to relate this page to mediafile.mediafile.
"""

from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms import extensions


class Extension(extensions.Extension):

    def handle_model(self):
        self.model.add_to_class(
            'media_files',
            models.ManyToManyField(
                'medialibrary.MediaFile',
                blank=True,
                null=True,
                help_text=_('Select media files that should be listed as related content.'),
            ),
        )

    def handle_modeladmin(self, modeladmin):
        modeladmin.extend_list('filter_horizontal', ['media_files'])

        modeladmin.add_extension_options(_('Media Files'), {
            'fields': ('media_files',),
            'classes': ('collapse',),
        })
