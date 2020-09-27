import typing as tp

from django.db.models import Model

from rest_framework.serializers import ValidationError


class PresentInDatasetValidator:

    def __init__(self,
                 model_class: Model,
                 model_param: tp.Optional[str] = None):
        self.model_class = model_class
        self.model_param = model_param

    def __call__(self, value):
        if self.model_param is not None:
            # check if objects with model_param=value exist
            query_filter = {self.model_param: value}
        else:
            # check not by field, but by the whole data
            query_filter = value
        if not self.model_class.objects.filter(**query_filter).exists():
            if self.model_param is not None:
                raise ValidationError(
                    f'There are no objects with {self.model_param} = {value} '
                    f'in model {self.model_class.__name__}')
            raise ValidationError(
                f'There are no objects like {str(query_filter)} '
                f'in model {self.model_class.__name__}')
