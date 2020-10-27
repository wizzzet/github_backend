from django.utils.translation import ugettext_lazy as _

from snippets.choices import StatusChoices


def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)


activate.short_description = _('Активировать')


def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)


deactivate.short_description = _('Деактивировать')


def draft(modeladmin, request, queryset):
    queryset.update(status=StatusChoices.DRAFT.value)


draft.short_description = _('В черновики')


def hide(modeladmin, request, queryset):
    queryset.update(status=StatusChoices.HIDDEN.value)


hide.short_description = _('Скрыть')


def publish(modeladmin, request, queryset):
    queryset.update(status=StatusChoices.PUBLIC.value)


publish.short_description = _('Опубликовать')
