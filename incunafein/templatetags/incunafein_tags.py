from django import template
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
        {% feincms_page_menu  feincms_page 'nav' 1 1 0 %}
    """
    def __init__(self,  feincms_page, css_id="", level=1, depth=1, show_all_subnav=False):
        self.feincms_page = feincms_page
        self.css_id = css_id
        self.level = level
        self.depth = depth
        self.show_all_subnav = show_all_subnav

    def render(self, context):
        feincms_page = self.feincms_page.resolve(context)

        level = int(self.level.resolve(context)if isinstance(self.level, template.FilterExpression) else self.level)
        depth = int(self.depth.resolve(context) if isinstance(self.depth, template.FilterExpression) else self.depth)
        css_id = self.css_id.resolve(context) if isinstance(self.css_id, template.FilterExpression) else self.css_id
        show_all_subnav = self.show_all_subnav.resolve(context) if isinstance(self.show_all_subnav, template.FilterExpression) else self.show_all_subnav

        request = context['request']
        entries = self.entries(feincms_page, level, depth, show_all_subnav)

        #context.push()
        #context['feincms_page'] =  feincms_page
        #context['css_id'] = css_id
        #context['level'] = level
        #context['depth'] = depth
        #context['entries'] = entries
        #output = template.loader.get_template('incunafein/page/menu.html').render(context)
        #context.pop()

        def get_item(item, next=None):
            context.push()

            context['item'] = item
            context['url'] = item.get_absolute_url()
            context['is_current'] = context['url'] == request.path
            context['title'] = item.title
            context['css_class'] = item.slug
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

        if not entries:
            return ''

        output = ''
        item = entries[0]
        for next in entries[1:]:
            output += get_item(item, next)
            item = next
            
        output += get_item(item)

        return '<ul id="%s">%s</ul>' % (css_id, output)

    def entries(self, instance, level=1, depth=1, show_all_subnav=False):
        if level <= 1:
            if depth == 1:
                return Page.objects.toplevel_navigation()
            elif show_all_subnav:
                return Page.objects.in_navigation().filter(level__lt=depth)
            else:
                return Page.objects.toplevel_navigation() | \
                        instance.get_ancestors().filter(in_navigation=True) | \
                        instance.get_siblings(include_self=True).filter(in_navigation=True, level__lt=depth) | \
                        instance.children.filter(in_navigation=True, level__lt=depth)

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
        elif show_all_subnav:
            queryset = instance.get_descendants().filter(level__lte=instance.level + depth, in_navigation=True)
            return PageManager.apply_active_filters(queryset)
        else:
            return instance.children.in_navigation() | \
                    instance.get_ancestors().filter(in_navigation=True, level__gte=level-1) | \
                    instance.get_siblings(include_self=True).filter(in_navigation=True, level__gte=level-1, level__lte=instance.level + depth)



def do_feincms_page_menu(parser, token):
    args = token.split_contents()
    if len(args) > 6:
        raise template.TemplateSyntaxError("'%s tag accepts no more than 5 arguments." % args[0])
    return FeincmsPageMenuNode(*map(parser.compile_filter, args[1:]))

register.tag('feincms_page_menu', do_feincms_page_menu)

