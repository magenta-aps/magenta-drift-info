from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Event, System, Customer, Server

admin.site.register(Event, SimpleHistoryAdmin)
admin.site.register(System, SimpleHistoryAdmin)
admin.site.register(Customer, SimpleHistoryAdmin)
admin.site.register(Server, SimpleHistoryAdmin)
