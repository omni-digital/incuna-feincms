from django.contrib import admin
from incunafein.admin import editor
from models import Navigation
from django import forms
#from django.conf import settings


class NavigationForm(forms.ModelForm):

    class Meta:
        models = Navigation

    def clean(self):
        cleaned_data = self.cleaned_data
        parent = cleaned_data.get("parent")
        page = cleaned_data.get("page")
        url = cleaned_data.get("url")
        title = cleaned_data.get("title")
        if parent:
            if (page and url) or (not (page or url)):
                msg = u"Provide either page or url (not both)."
                self._errors["page"] = self.error_class([msg])
                self._errors["url"] = self.error_class([msg])
     
                del cleaned_data["page"]
                del cleaned_data["url"]

            elif url and not title:
                msg = u"Provide a title for the url."
                self._errors["url"] = self.error_class([msg])
                self._errors["title"] = self.error_class([msg])
     
                del cleaned_data["url"]
                del cleaned_data["title"]
        else:
            if not cleaned_data.get("dom_id"):
                msg = u"Provide a Dom id for the (top level) navigation."
                self._errors["parent"] = self.error_class([msg])
                self._errors["dom_id"] = self.error_class([msg])
     
                del cleaned_data["parent"]
                del cleaned_data["dom_id"]


        return cleaned_data

class NavigationAdmin(editor.TreeEditor):
    list_display = ('__unicode__', )
    list_filter = ('parent',)
    form = NavigationForm

admin.site.register(Navigation, NavigationAdmin)

