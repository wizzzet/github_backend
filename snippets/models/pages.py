from django.db import models

from solo.models import SingletonModel

from snippets.models import BasicModel, LastModMixin
from snippets.models.seo import SEOModelMixin


class BasePage(SEOModelMixin, LastModMixin, SingletonModel, BasicModel):
    """Базовая модель страниц"""

    title = models.CharField('Заголовок', max_length=255, blank=True, null=True)

    translation_fields = SEOModelMixin.translation_fields + ('title',)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title if self.title else ''
