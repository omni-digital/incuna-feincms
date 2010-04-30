from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

register = template.Library()

class GetFeincmsPageNode(template.Node):
    """
    example usage:
        {% get_feincms_page path as varname %}
    """
    def __init__(self, path, var_name):
        self.path = template.Variable(path)
        self.var_name = var_name

    def render(self, context):
        self.path = self.path.resolve(context)
        from feincms.module.page.models import Page
        try: 
            context[self.var_name] = Page.objects.page_for_path(path=self.path)
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