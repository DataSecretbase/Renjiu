from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Video)
admin.site.register(HTML5Video)
admin.site.register(VideoCategory)

admin.site.register(Audio)
admin.site.register(HTML5Audio)
admin.site.register(AudioCategory)

admin.site.register(Category)
admin.site.register(Node)
admin.site.register(Topic)
admin.site.register(Comment)
admin.site.register(IndexTopic)
