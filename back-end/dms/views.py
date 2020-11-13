from django.utils.decorators import method_decorator

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.status import HTTP_422_UNPROCESSABLE_ENTITY
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from drf_yasg.utils import swagger_auto_schema

from django_filters.rest_framework import DjangoFilterBackend

from taggit.models import Tag

from dms.filters import PaperFilter
from dms.parsers import MultiPartWithJSONParser
from dms.swagger import AUTHOR_ARRAY
from dms.serializers import (
    AuthorSerializer,
    BookMutateSerializer,
    BookSerializer,
    CategorySerializer,
    ClassMaterialMutateSerializer,
    ClassMaterialSerializer,
    PaperMutateSerializer,
    PaperSerializer,
    PublisherSerializer,
    SectionRetrieveSerializer,
    SectionSerializer,
    SubjectRetrieveSerializer,
    OrderUpdateSerializer,
    SubjectSerializer,
    TagSerializer,
    TopicSerializer,
    TopicRetrieveSerializer,
)
from dms.models import (
    Author,
    Book,
    Category,
    ClassMaterial,
    Paper,
    Publisher,
    Section,
    Subject,
    Topic,
)
from dms.permissions import (
    ReadOnly,
    IsOwner,
)

MUTATE_ACTIONS = ["create", "update", "partial_update"]


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    def destroy(self, request, *args, **kwargs):
        category = self.get_object()

        if Paper.objects.filter(category=category).exists():
            return Response(
                {"message": "Category has documents and can not be deleted."},
                status=HTTP_422_UNPROCESSABLE_ENTITY)

        return super().destroy(request, *args, **kwargs)


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.AllowAny]


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [SearchFilter]
    search_fields = ["title", "annotation"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SubjectRetrieveSerializer
        return SubjectSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SectionRetrieveSerializer
        return SectionSerializer


class OrderUpdateAPIView(generics.GenericAPIView, mixins.UpdateModelMixin):
    permission_classes = [permissions.AllowAny]
    serializer_class = OrderUpdateSerializer
    lookup_field = "id"

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class SectionOrderUpdateAPIView(OrderUpdateAPIView):
    queryset = Section.objects.all()


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TopicRetrieveSerializer
        return TopicSerializer


class TopicOrderUpdateAPIView(OrderUpdateAPIView):
    queryset = Topic.objects.all()


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(manual_parameters=[AUTHOR_ARRAY]))
class PaperViewSet(viewsets.ModelViewSet):
    queryset = Paper.objects.order_by("-publication_date", "title")
    permission_classes = [ReadOnly | IsOwner]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PaperFilter
    search_fields = ["title", "annotation", "tags__name"]
    parser_classes = [MultiPartWithJSONParser, JSONParser]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return PaperMutateSerializer
        return PaperSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [ReadOnly | IsOwner]
    filter_backends = [OrderingFilter]
    ordering_fields = ["title", "publication_year"]
    parser_classes = [MultiPartWithJSONParser, JSONParser]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return BookMutateSerializer
        return BookSerializer


class ClassMaterialViewSet(viewsets.ModelViewSet):
    queryset = ClassMaterial.objects.all()
    permission_classes = [ReadOnly | IsOwner]
    parser_classes = [MultiPartWithJSONParser, JSONParser]

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return ClassMaterialMutateSerializer
        return ClassMaterialSerializer
