from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template import RequestContext
from django.template.loader import render_to_string


class BaseFkeyContent(models.Model):
    
    """ Returns a generic fkey Feincontent type for the simple case where you want to add a foreignkey to another object.
    
    You can use this directly with create_content_type:

    from incunafein.content import fkeycontent_factory
    from locations.models import LocationCategory    
    Page.create_content_type(fkeycontent_factory(LocationCategory, fkey_name='location_category'))

    
    """

    class Meta:
        abstract = True

    @classmethod
    def initialize_type(cls):
        if cls.app_label not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured, "You have to add '%s' to your INSTALLED_APPS before creating a %s" % (cls.app_label, cls.__name__)

        cls.add_to_class(cls.fkey_name or cls.object_name.lower(),
            models.ForeignKey('%s.%s' % (cls.app_label, cls.object_name),
            related_name='%s_%s_set' % (cls._meta.app_label, cls._meta.module_name)
        ))
        
    def template_hierarchy(self):
        return ['content/%s/%s.html' % (self.app_label, self.fkey_name or self.object_name.lower()),
                'content/%s/default.html' % self.app_label,
                ]

    def render(self, request=None, **kwargs):
        if request is not None:
            context = RequestContext(request)
            context.update({ 'content': self })
        else:
            context = { 'content': self }

        return render_to_string(self.template_hierarchy(), context)


def fkeycontent_factory(model, content=BaseFkeyContent, model_name=None, fkey_name=None):
    """Return a BaseFkeyContent for the label and name class."""
    opts = model._meta
    
    class Meta:
        abstract = True
    
    attrs = {'app_label': opts.app_label,
             'object_name': opts.object_name,
             'fkey_name': fkey_name,
             '__module__': model.__module__,
             'Meta': Meta,
             
            }
    return type(model_name or model.__name__  + 'Content', (content,), attrs)
