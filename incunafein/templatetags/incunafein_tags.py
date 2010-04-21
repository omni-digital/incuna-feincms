from django.core.urlresolvers import reverse
from django.conf import settings
from django import template

register = template.Library()

class GetFeincmsPageNode(template.Node):
    def __init__(self, slug, var_name):        
        self.slug = template.Variable(slug)
        self.var_name = var_name

    def render(self, context):
        self.slug = self.slug.resolve(context)
        from feincms.module.page.models import Page
        try: 
            context[self.var_name] = Page.objects.get(slug=self.slug)
        except Page.DoesNotExist:
            pass

        return u''

def get_feincms_page(parser, token):
    bits = token.contents.split()
    if len(bits) != 4:
        raise template.TemplateSyntaxError("'%s' tag takes three arguments" % bits[0])
    if bits[2] != 'as':
        raise template.TemplateSyntaxError("second argument to '%s' tag must be 'as'" % bits[0])

    return GetFeincmsPageNode(bits[1], bits[3])

register.tag('get_feincms_page', get_feincms_page)