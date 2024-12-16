from django.contrib import admin
from .models import (
    User,
    Mode,
    Prompt,
    Transaction,
    UserMode,
    TrainingMaterial
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
    list_display = ['telegram_id', 'name', 'plan_end', ]
    list_display_links = ['telegram_id', ]
    search_fields = ['telegram_id', 'name', ]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'cash', ]
    list_display_links = ['user', ]
    search_fields = ['user', 'cash', ]


class UserPlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'renew_date']
    list_display_links = ['user', ]
    search_fields = ['user', ]


class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', ]
    list_display_links = ['name', ]
    search_fields = ['name', ]


class UserModeAdmin(admin.ModelAdmin):
    list_display = ['modes_request', 'user']


class TrainingMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at', 'agree_text', 'numeration')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')
    list_editable = ('agree_text', 'numeration')


admin.site.register(Mode, ModeAdmin)
admin.site.register(Prompt, PromptAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(TrainingMaterial, TrainingMaterialAdmin)
admin.site.register(UserMode, UserModeAdmin)
