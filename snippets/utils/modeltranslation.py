from django.conf import settings

from modeltranslation.translator import TranslationOptions


class BaseTranslationOptions(TranslationOptions):
    required_languages = (settings.DEFAULT_LANGUAGE,)
    fallback_undefined = ''
    empty_values = ''


def get_model_translation_fields(model, with_original_fields=True):
    fields = []
    if with_original_fields:
        fields.extend(model.translation_fields)

    for language in settings.LANGUAGE_CODES:
        fields.extend('%s_%s' % (x, language) for x in model.translation_fields)

    return fields
