from django.contrib import admin
from .models import Event, Logbook, LogEntry, MirrorLogbook

# Rekisteröidään mallit, jotta niitä voidaan hallinnoida Djangon admin-paneelissa
admin.site.register(Event)
admin.site.register(Logbook)
admin.site.register(LogEntry)
admin.site.register(MirrorLogbook)
