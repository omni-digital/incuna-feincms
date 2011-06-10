from django.contrib import admin
from django.db import models
from feincms.module.medialibrary.models import MediaFile

VIDEO_TYPE = 'video'

class VideoChapter(models.Model):
    video = models.ForeignKey('medialibrary.MediaFile', limit_choices_to = {'type': VIDEO_TYPE})
    title = models.CharField(max_length=255)
    timecode = models.TimeField(help_text='hh:mm:ss')
    preview = models.ImageField(upload_to='medialibrary/section/', null=True, blank=True)

    class Meta:
        app_label = 'medialibrary'
        ordering = ('timecode',)

    def __unicode__(self):
        return self.title

    @property
    def seconds(self):
        return self.timecode.hour*3600+self.timecode.minute*60+self.timecode.second

class VideoChapterAdmin(admin.ModelAdmin):
    list_display      = ['video', 'title', 'timecode']
    list_filter       = ['video']
    search_fields     = ['title']


