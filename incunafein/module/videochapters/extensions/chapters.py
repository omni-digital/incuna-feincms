from incunafein.module.videochapters.models import VideoChapter
def register(cls, admin_cls):
    if admin_cls:
        from django.contrib import admin
        class VideoChaptersInline(admin.TabularInline):
            model = VideoChapter
            extra = 3

        admin_cls.inlines = list(admin_cls.inlines) + [VideoChaptersInline, ]
