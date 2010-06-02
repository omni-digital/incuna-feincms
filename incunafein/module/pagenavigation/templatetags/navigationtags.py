from django import template
#from feincms.module.page.models import Page, PageManager
from incunafein.module.pagenavigation.models import Navigation#, NavigationManage

register = template.Library()
class IncunaFeinNavigationNode(template.Node):
    """
    example usage:
        {% incunafein_navigation navigate %}
    """
    def __init__(self,  navigate):
        self.navigate = navigate

    def render(self, context):
        navigate = self.navigate.resolve(context)

        if isinstance(navigate, Navigation):
            instance = navigate
        elif isinstance(navigate, (str, unicode)):
            try:
                instance = Navigation.objects.get(dom_id=navigate)
            except Navigation.DoesNotExist:
                instance = None

        context.push()
        context['instance'] =  instance
        context['css_id'] = getattr(instance, 'dom_id', '')
        if instance is None:
            context['entries'] = objects.filter(parent__isnull=True)
        else:
            context['entries'] = instance.children.all()

        output = template.loader.get_template('navigation/navigation.html').render(context)
        context.pop()

        return output

def do_incunafein_navigation(parser, token):
    args = token.split_contents()
    if len(args) > 2:
        raise template.TemplateSyntaxError("'%s tag accepts no more than 1 argument." % args[0])
    return IncunaFeinNavigationNode(*map(parser.compile_filter, args[1:]))

register.tag('incunafein_navigation', do_incunafein_navigation)


