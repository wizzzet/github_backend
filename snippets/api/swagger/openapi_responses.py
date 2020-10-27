from drf_yasg.openapi import Response as OpenApiResponse

from snippets.api.swagger import serializers


success_response = OpenApiResponse(
    'Успешный ответ',
    serializers.SuccessResponseSerializer
)


validation_error_response = OpenApiResponse(
    'Ответ с ошибками валидации',
    serializers.ValidationErrorResponseSerializer
)
