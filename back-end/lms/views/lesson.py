from datetime import datetime

from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from lms.models.common import Milgroup
from lms.models.lesson import Lesson
from lms.serializers.common import MilgroupSerializer
from lms.serializers.lesson import (LessonSerializer,
                                    LessonJournalGetQuerySerializer)
from lms.filters.lesson import LessonFilter
from lms.functions import get_date_range


@extend_schema(tags=['lesson'])
class LessonViewSet(ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]

    filterset_class = LessonFilter


@extend_schema(tags=['lesson-journal'],
               parameters=[
                   OpenApiParameter(name='milgroup',
                                    description='Filter by milgroup',
                                    required=True,
                                    type=int),
                   OpenApiParameter(name='date_from',
                                    description='Filter by date',
                                    required=True,
                                    type=OpenApiTypes.DATE),
                   OpenApiParameter(name='date_to',
                                    description='Filter by date',
                                    required=True,
                                    type=OpenApiTypes.DATE),
               ])
class LessonJournalView(GenericAPIView):
    permission_classes = [AllowAny]

    # pylint: disable=too-many-locals
    def get(self, request: Request) -> Response:
        query_params = LessonJournalGetQuerySerializer(
            data=request.query_params)
        if not query_params.is_valid():
            return Response(query_params.errors, status=HTTP_400_BAD_REQUEST)

        # final json
        data = {}

        # add milgroup data
        milgroup = MilgroupSerializer(
            Milgroup.objects.get(
                milgroup=request.query_params['milgroup'])).data
        data['milgroup'] = milgroup

        # calculate dates
        date_from = datetime.fromisoformat((query_params.data['date_from']))
        date_to = datetime.fromisoformat((query_params.data['date_to']))

        date_range = get_date_range(date_from, date_to, milgroup['weekday'])
        data['dates'] = date_range

        # sort lessons by date and milgroup
        lessons_filtered = Lesson.objects.filter(
            milgroup=request.query_params['milgroup'],
            date__gte=request.query_params['date_from'],
            date__lte=request.query_params['date_to'])

        # ordinals
        ordinals = []
        for ordinal in range(1, 11):
            lessons = dict()
            lessons['ordinal'] = ordinal
            lessons['lessons'] = LessonSerializer(
                lessons_filtered.filter(ordinal=ordinal), many=True).data
            ordinals.append(lessons)

        data['ordinals'] = ordinals

        return Response(data, status=HTTP_200_OK)
