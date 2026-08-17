from django.contrib import admin

from .models import Alert, AutomationExecution, AutomationRule

admin.site.register(Alert)
admin.site.register(AutomationRule)
admin.site.register(AutomationExecution)
