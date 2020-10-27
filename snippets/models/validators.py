def validate_svg_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.svg']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Файл не в формате SVG')
