from collections import OrderedDict
from smtplib import SMTPException
import traceback

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string

from markupsafe import escape

from vars.models import SiteConfig


def get_admin_emails(request=None, force_system=False, field='admins'):

    if force_system:
        return [x[1] for x in settings.ADMINS]

    admins = getattr(SiteConfig.get_solo(), field, None)
    return admins.split(',') if admins else [x[1] for x in settings.ADMINS]


def get_default_from_email():
    return settings.DEFAULT_FROM_EMAIL


def send_email(template, emails, subject, params=None, extra_headers=None, from_email=None,
               raise_error=True):

    if from_email is None:
        from_email = get_default_from_email()

    if params is None:
        params = {}

    params.update(
        site=settings.SITE_NAME,
        site_url=settings.SITE_URL
    )

    message_html = render_to_string(
        'emails/%s/%s.html' % (template, template), params
    )
    message_txt = render_to_string(
        'emails/%s/%s.txt' % (template, template), params
    )

    msg = EmailMultiAlternatives(subject, message_txt, from_email, emails, headers=extra_headers)
    msg.attach_alternative(message_html, 'text/html')
    try:
        return msg.send()
    except (SMTPException, ConnectionError):
        print(traceback.format_exc())
        if raise_error:
            raise
    return 0


def send_trigger_email(event, request=None, obj=None, fields=None, emails=None, from_email=None,
                       extra_data=None, extra_headers=None, raise_error=False):
    if emails is None:
        emails = get_admin_emails(request=request)

    if from_email is None:
        from_email = get_default_from_email()

    if event is None:
        if obj:
            event = 'новый объект {obj}'.format(obj=obj._meta.verbose_name)
        else:
            event = 'новое событие'

    if extra_data is not None:
        assert isinstance(extra_data, dict)

    subject = '{event} на сайте {site}'.format(site=settings.SITE_NAME, event=event)

    site_url = settings.ADMIN_SITE_URL \
        if hasattr(settings, 'ADMIN_SITE_URL') else settings.SITE_URL

    admin_url = None
    if obj:
        meta = obj._meta
        model = meta.model
        app = model.__module__.split('.')[0]
        model_name = meta.object_name.lower()

        if fields is None:
            fields = {'ID': obj.pk}
        else:
            field_names = fields[:]
            fields = OrderedDict()
            for field in field_names:
                if isinstance(field, (list, tuple)):
                    value = getattr(obj, field[0])
                    fields[str(field[1])] = value
                    continue
                else:
                    value = getattr(obj, field)

                for f in meta.fields:
                    if f.name == field:
                        if isinstance(f, models.ForeignKey):
                            if value:
                                orig_value = value
                                value = 'ID=%s: %s' % (value.id, escape(str(value)))

                                if hasattr(orig_value, 'get_absolute_url'):
                                    value = '<a href="%s%s">%s</a>' % (
                                        site_url,
                                        orig_value.get_absolute_url(),
                                        value
                                    )
                            else:
                                value = '-'
                        else:
                            value = escape(value)
                        fields[f.verbose_name] = value
                        break

        admin_url = '/%s/%s/%s/change/' % (app, model_name, obj.pk)

    params = {
        'admin_url': admin_url,
        'extra_data': extra_data,
        'fields': fields,
        'site_url': site_url,
        'subject': subject
    }

    message_txt = render_to_string(
        'emails/admin/new_object_trigger.html',
        params
    )

    msg = EmailMessage(
        subject, message_txt, from_email, emails, headers=extra_headers
    )

    result = 0
    try:
        result = msg.send()
    except (SMTPException, ConnectionError):
        print(traceback.format_exc())
        if raise_error:
            raise
    return result
