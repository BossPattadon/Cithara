from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(SongCreator)
admin.site.register(Listener)
admin.site.register(Library)
admin.site.register(Song)
admin.site.register(SongGeneration)
admin.site.register(ShareLink)
