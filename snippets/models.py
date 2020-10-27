from django.db import models
from django.utils.translation import ugettext_lazy as _

from solo.models import SingletonModel

from snippets.models import LastModMixin, BasicModel
from snippets.models.seo import SEOModelMixin


class BasePage(SEOModelMixin, LastModMixin, BasicModel, SingletonModel):
    """Base page model"""
    title = models.CharField(_('Заголовок'), max_length=255, blank=True, null=True)

    translation_fields = ('title',)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title
