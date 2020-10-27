from modeltranslation.admin import TranslationAdmin, TranslationStackedInline

from snippets.admin import BaseModelAdmin
from snippets.models.articles import BaseArticle
from snippets.utils.modeltranslation import get_model_translation_fields


class BaseArticleAdmin(BaseModelAdmin, TranslationAdmin):
    """Базовая админ.часть для новостей и событий"""

    date_hierarchy = 'publish_date'
    list_display = ('id', 'image_thumb', 'title', 'publish_date', 'ordering', 'status', 'updated')
    list_display_links = ('id', 'image_thumb', 'title')
    list_editable = ('status', 'ordering', 'publish_date')
    ordering = ('ordering', '-publish_date')
    search_fields = ['=id', 'slug', 'image'] + get_model_translation_fields(BaseArticle)
    suit_form_tabs = (
        ('general', 'Основное'),
        ('body', 'Основной контент'),
        ('sections', 'Секции'),
        ('seo', 'SEO')
    )

    class Media:
        js = ('admin/js/translit.js',)


class BaseArticleSectionInline(TranslationStackedInline):
    """Базовая админ.часть для входимой админки секций статей"""

    extra = 0
    ordering = ('ordering',)
    raw_id_fields = ('gallery',)
    readonly_fields = ('created', 'updated')
    suit_classes = 'suit-tab suit-tab-sections'
