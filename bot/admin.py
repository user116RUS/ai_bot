from django.contrib import admin
from .models import (
    User,
    Mode,
    Referal,
    Prompt,
    Transaction,

)


class ModeAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'max_token', ]
    list_display_links = ['name']
    search_fields = ['name', 'model', ]
    ordering = ['max_token', ]


class PromptAdmin(admin.ModelAdmin):
    list_display = ['text', 'name', ]
    list_display_links = ['name', ]
    search_fields = ['name', ]


class ReferalAdmin(admin.ModelAdmin):
    list_display = ['inviter', 'is_used', ]
    search_fields = ['inviter', ]
    ordering = ['is_used', ]


class UserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'name', ]
    list_display_links = ['telegram_id', ]
    search_fields = ['telegram_id', 'name', ]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'cash', 'mode', ]
    list_display_links = ['buyer', ]
    search_fields = ['buyer', 'cash', 'mode', ]


admin.site.register(Mode, ModeAdmin)
admin.site.register(Prompt, PromptAdmin)
admin.site.register(Referal, ReferalAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Transaction, TransactionAdmin)
