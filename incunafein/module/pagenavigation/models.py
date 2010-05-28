from django.db import models
import mptt

class Navigation(models.Model):
   """Navigation item. uses mptt so can have sub navigation."""

   page = models.ForeignKey('page.Page', null=True, blank=True)
   title = models.CharField(max_length=250, null=True, blank=True, help_text="Leave blank to use the page title.")
   url = models.URLField(verify_exists=False, max_length=250, null=True, blank=True, help_text="Set either the page or url.")
   parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
   css_class = models.CharField(max_length=250, null=True, blank=True)
   dom_id = models.CharField(max_length=250, null=True, blank=True)

   class Meta:
       ordering = ['tree_id', 'lft']

   def __unicode__(self):
       return u"%s" % (self.title or self.page or self.url or self.dom_id,)


   def get_absolute_url(self):
       return u"%s" % (self.page and self.page.get_absolute_url() or self.url,)

mptt.register(Navigation)

