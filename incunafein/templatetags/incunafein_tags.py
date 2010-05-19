from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from feincms.module.page.models import Page, PageManager

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

class FeincmsPageMenuNode(template.Node):
    """
    example usage:
        {% feincms_page_menu  feincms_page css_id level depth %}
    """
    def __init__(self,  feincms_page, css_id="", level=1, depth=1):
        self.feincms_page = feincms_page
        #self.level = template.Variable(level)
        #self.depth = template.Variable(depth)
        self.level = level
        self.depth = depth
        self.css_id = css_id

    def render(self, context):
        feincms_page = self.feincms_page.resolve(context)
        level = int(isinstance(self.level, template.FilterExpression) and self.level.resolve(context) or self.level)
        depth = int(isinstance(self.depth, template.FilterExpression) and self.depth.resolve(context) or self.depth)
        css_id = isinstance(self.css_id, template.FilterExpression) and self.css_id.resolve(context) or self.css_id

        context.push()
        context['feincms_page'] =  feincms_page
        context['css_id'] = css_id
        context['level'] = level
        context['depth'] = depth
        context['entries'] = self.entries(feincms_page, level, depth)

        output = template.loader.get_template('incunafein/page/menu.html').render(context)
        context.pop()

        return output

    def entries(self, instance, level=1, depth=1):
        if level <= 1:
            if depth == 1:
                return Page.objects.toplevel_navigation()
            else:
                return Page.objects.in_navigation().filter(level__lt=depth)

        # mptt starts counting at 0, NavigationNode at 1; if we need the submenu
        # of the current page, we have to add 2 to the mptt level
        if instance.level + 2 == level:
            pass
        elif instance.level + 2 < level:
            try:
                queryset = instance.get_descendants().filter(level=level - 2, in_navigation=True)
                instance = PageManager.apply_active_filters(queryset)[0]
            except IndexError:
                return []
        else:
            instance = instance.get_ancestors()[level - 2]


        if depth == 1:
            return instance.children.in_navigation()
        else:
            queryset = instance.get_descendants().filter(level__lte=instance.level + depth, in_navigation=True)
            return PageManager.apply_active_filters(queryset)


def do_feincms_page_menu(parser, token):
    args = token.split_contents()
    if len(args) > 5:
        raise template.TemplateSyntaxError("'%s tag accepts no more than 4 arguments." % args[0])
    return FeincmsPageMenuNode(*map(parser.compile_filter, args[1:]))

register.tag('feincms_page_menu', do_feincms_page_menu)

