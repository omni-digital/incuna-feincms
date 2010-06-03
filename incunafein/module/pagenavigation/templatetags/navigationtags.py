from django.db.models import Q
from django import template
#from feincms.module.page.models import Page, PageManager
from incunafein.module.pagenavigation.models import Navigation#, NavigationManage

register = template.Library()
class IncunaFeinNavigationNode(template.Node):
    """
    Render a navigation.
    Arguments: 
        navigate: The root item (instance or dom_id) of the navigation to render.
        depth: the depth of sub navigation to include.
        show_all_subnav: Whether to show all sub navigation items (or just the ones in the currently selected branch).

    example usage:
        {% incunafein_navigation 'footer' 1 0 %}
    """
    def __init__(self,  navigate=None, depth=1, show_all_subnav=False):
        self.navigate = navigate
        self.depth = depth
        self.show_all_subnav = show_all_subnav

    def render(self, context):
        navigate = self.navigate and self.navigate.resolve(context)
        depth = int(self.depth.resolve(context) if isinstance(self.depth, template.FilterExpression) else self.depth)
        show_all_subnav = self.show_all_subnav.resolve(context) if isinstance(self.show_all_subnav, template.FilterExpression) else self.show_all_subnav

        instance = None
        if isinstance(navigate, Navigation):
            instance = navigate
        elif isinstance(navigate, (str, unicode)) and navigate:
            try:
                instance = Navigation.objects.get(dom_id=navigate)
            except Navigation.DoesNotExist:
                pass

        if not 'request' in context:
            raise ValueError("No request in the context. Try using RequestContext in the view.")
        path = context['request'].path

        try:
            current = Navigation.objects.filter(Q(url=path) | Q(page___cached_url=path))[0]
        except IndexError:
            current = None

        entries = self.entries(instance, current, depth, show_all_subnav)

        print entries

        if not entries:
            return ''

        #context.push()
        #context['instance'] =  instance
        #context['css_id'] = getattr(instance, 'dom_id', '')
        #if instance is None:
        #    context['entries'] = Navigation.objects.filter(parent__isnull=True)
        #else:
        #    context['entries'] = instance.children.all()

        #output = template.loader.get_template('navigation/navigation.html').render(context)
        #context.pop()

        #return output

        def get_item(item, next=None):
            context.push()

            context['item'] = item
            context['url'] = item.get_absolute_url()
            context['is_current'] = context['url'] == path
            context['title'] = unicode(item)
            context['css_class'] = item.css_class
            if context['is_current']:
                context['css_class'] += ' selected'

            if next:
                if next.level > item.level:
                    context['down'] = True
                elif next.level < item.level:
                    context['up'] = True

            html = template.loader.get_template('incunafein/page/menuitem.html').render(context)
            context.pop()

            return html

        output = ''
        item = entries[0]
        for next in entries[1:]:
            output += get_item(item, next)
            item = next
            
        output += get_item(item)

        if instance:
            return '<ul id="%s" class="%s">%s</ul>' % (instance.dom_id, instance.css_class, output)
        else:
            return '<ul>%s</ul>' % (output,)


    def entries(self, instance, current, depth=1, show_all_subnav=False):
        #if instance is None:
        #    return Navigation.objects.filter(parent__isnull=True)
        #else:
        #    return instance.children.all()

        if depth == 1:
            #return Page.objects.toplevel_navigation()
            if instance is None:
                return Navigation.objects.filter(parent__isnull=True)
            else:
                return instance.children.all()
        elif show_all_subnav:
            #return Page.objects.in_navigation().filter(level__lt=depth)
            if instance is None:
                return Navigation.objects.all()
            else:
                return instance.get_descendants()
        else:
            #return Page.objects.toplevel_navigation() | \
            #        instance.get_ancestors().filter(in_navigation=True) | \
            #        instance.get_siblings(include_self=True).filter(in_navigation=True, level__lt=depth) | \
            #        instance.children.filter(in_navigation=True, level__lt=depth)
            if instance is None:
                qs = Navigation.objects.filter(parent__isnull=True) 
                if current:
                    qs = qs | current.get_ancestors() \
                            | current.get_siblings(include_self=True).filter(level__lt=depth) \
                            | current.children.filter(level__lt=depth)
            else:
                #return instance.children.all()
                relative_depth = instance.level + depth
                qs = instance.children.all()
                if current:
                    qs = qs | current.get_ancestors().filter(level__gt=instance.level) \
                            | current.get_siblings(include_self=True).filter(level__gt=instance.level, level__lt=relative_depth) \
                            | current.children.filter(level__gt=instance.level, level__lt=relative_depth)
            return qs

def do_incunafein_navigation(parser, token):
    args = token.split_contents()
    if len(args) > 4:
        raise template.TemplateSyntaxError("'%s tag accepts no more than 3 argument." % args[0])
    return IncunaFeinNavigationNode(*map(parser.compile_filter, args[1:]))

register.tag('incunafein_navigation', do_incunafein_navigation)


