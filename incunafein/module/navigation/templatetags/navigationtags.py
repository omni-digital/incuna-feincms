import warnings

from django.db.models import Q
from django import template
from incunafein.module.navigation.models import Navigation

register = template.Library()


class IncunaFeinNavigationNode(template.Node):
    """
    Render a navigation.
    arguments:
        navigate: The root item (instance or dom_id) of the navigation
            to render.
        depth: The depth of sub navigation to include.
        show_all_subnav: Whether to show all sub navigation items
            (or just the ones in the currently selected branch).

    example usage:
        {% incunafein_navigation 'footer' 1 0 %}
    """
    def __init__(self,  navigate=None, depth=1, show_all_subnav=False):
        self.navigate = navigate
        self.depth = depth
        self.show_all_subnav = show_all_subnav

    def render(self, context):
        navigate = self.navigate and self.navigate.resolve(context)

        if isinstance(self.depth, template.base.FilterExpression):
            depth = int(self.depth.resolve(context))
        else:
            depth = int(self.depth)

        if isinstance(self.show_all_subnav, template.base.FilterExpression):
            show_all_subnav = self.show_all_subnav.resolve(context)
        else:
            show_all_subnav = self.show_all_subnav

        instance = None
        if isinstance(navigate, Navigation):
            instance = navigate
        elif isinstance(navigate, (str, unicode)) and navigate:
            try:
                instance = Navigation.objects.get(dom_id=navigate)
            except Navigation.DoesNotExist:
                return ''

        if 'request' not in context:
            msg = 'No request in the context. Try using RequestContext in the view.'
            warnings.warn(msg)
            return ''
        path = context['request'].path

        try:
            current = Navigation.objects.filter(
                Q(url=path) | Q(page___cached_url=path),
            )[0]
        except IndexError:
            current = None

        entries = self.entries(instance, current, depth, show_all_subnav)

        if not entries:
            return ''

        def get_item(item, next_level, extra_context=None):
            url = item.get_absolute_url()
            internal_context = {
                'item': item,
                'level': item.level,
                'url': url,
                'is_current': url == path,
                'title': unicode(item),
            }
            if extra_context:
                internal_context.update(extra_context)

            css_class = item.css_class or (item.page and item.page.slug) or ''
            if css_class:
                if 'css_class' in internal_context:
                    internal_context['css_class'] += ' ' + css_class
                else:
                    internal_context['css_class'] = css_class

            internal_context['is_ancestor'] = False
            if internal_context['is_current']:
                if 'css_class' in internal_context:
                    internal_context['css_class'] += ' selected'
                else:
                    internal_context['css_class'] = 'selected'
            else:
                internal_context['is_ancestor'] = path.startswith(url)

            if next_level > item.level:
                internal_context['down'] = next_level - item.level
            elif next_level < item.level:
                internal_context['up'] = item.level - next_level

            navitem = template.loader.get_template('navigation/navitem.html')
            html = navitem.render(internal_context)

            return html

        output = ''
        item = entries[0]
        for i, next in enumerate(entries[1:]):
            output += get_item(item, next.level, {'css_class': i == 0 and 'first' or ''})
            item = next

        output += get_item(item, entries[0].level, {'css_class': len(entries) == 1 and 'first last' or 'last'})

        if instance:
            return '<ul id="{}" class="{}">{}</ul>'.format(instance.dom_id, instance.css_class, output)
        else:
            return '<ul>{}</ul>'.format(output)

    def entries(self, instance, current, depth=1, show_all_subnav=False):

        if depth == 1:
            if instance is None:
                return Navigation.objects.filter(parent__isnull=True)
            else:
                return instance.children.all()
        elif show_all_subnav:
            if instance is None:
                return Navigation.objects.filter(level__lt=depth)
            else:
                return instance.get_descendants().filter(level__lt=depth)
        else:
            if instance is None:
                qs = Navigation.objects.filter(parent__isnull=True)
                if current:
                    siblings = current.get_siblings(include_self=True)
                    filtered_siblings = siblings.filter(level__lt=depth)

                    qs |= current.get_ancestors()
                    qs |= filtered_siblings
                    qs |= current.children.filter(level__lt=depth)
            else:
                relative_depth = instance.level + depth
                qs = instance.children.all()
                if current:
                    siblings = current.get_siblings(include_self=True)
                    filtered_siblings = siblings.filter(
                        level__gt=instance.level,
                        level__lt=relative_depth,
                    )
                    children = current.children.filter(
                        level__gt=instance.level,
                        level__lt=relative_depth,
                    )

                    qs |= current.get_ancestors().filter(level__gt=instance.level)
                    qs |= filtered_siblings
                    qs |= children
            return qs


def do_incunafein_navigation(parser, token):
    args = token.split_contents()
    if len(args) > 4:
        raise template.TemplateSyntaxError(
            "'%s tag accepts no more than 3 argument." % args[0],
        )
    return IncunaFeinNavigationNode(*map(parser.compile_filter, args[1:]))

register.tag('incunafein_navigation', do_incunafein_navigation)
