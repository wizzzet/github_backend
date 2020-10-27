from django.db import models

from django.utils.translation import ugettext_lazy as _


class PaymentStatusChoices(models.IntegerChoices):
    """Статусы оплаты"""

    NOT_PAID = -1, _('Не оплачено')
    PAID = 1, _('Оплачено')


class StatusChoices(models.IntegerChoices):
    """
    Object publicity status enumerate
    """

    DRAFT = 0, _('Черновик')
    PUBLIC = 1, _('Публичный')
    HIDDEN = 2, _('Скрытый')
