import operator

from functools import reduce

from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.models.functions import ExtractYear
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from backend.models import (
    Document,
    Profile,
    Publisher,
    Subject,
)


@permission_classes((AllowAny,))
class UploadNirView(APIView):
    parser_classes = (
        FileUploadParser,
    )

    def put(self, request):
        """
        Usage PUT request to api/upload?type=nir&id=21
        curl -X PUT -H 'Content-Disposition: attachment; filename=ptu.png' 'http://127.0.0.1:8000/api/upload?id=1' --upload-file Колледж\ ПТУ.png
        :param request:
        :return:
        """

        if "file" not in request.data:
            return Response(
                {
                    "error": "No file provided",
                },
                status=HTTP_400_BAD_REQUEST,
            )

        doc = Document.objects.all()
        f = request.data["file"]
        doc.get(
            pk=request.query_params.get("id")
        ).file.save(
            name=f.name,
            content=f,
            save=True,
        )

        return Response(
            {
                "code": HTTP_201_CREATED * 100,
            },
            status=HTTP_201_CREATED,
        )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def get_file(request):
    """
    Usage: api/get_file?type=nir&id=3
    :param request:
    :return:
    """
    doc = Document.objects.all()
    f = doc.get(pk=request.query_params.get("id")).file
    filename = f.name.split('/')[-1]
    response = HttpResponse(f.path, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response(
            {
                "error": "Please provide both username and password"
            },
            status=HTTP_400_BAD_REQUEST,
        )

    user = authenticate(
        username=username,
        password=password,
    )
    if not user:
        return Response(
            {
                "error": "Invalid Credentials"
            },
            status=HTTP_404_NOT_FOUND,
        )

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": {
                "token": token.key
            }
        },
        status=HTTP_200_OK,
    )


@csrf_exempt
@api_view(["GET"])
def info(request):
    data = {
        "roles": ["admin"],
        "avatar": request.user.profile.photo,
        "name": request.user.profile.name,
    }

    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": data
        },
        status=HTTP_200_OK,
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def logout(request):
    try:
        request.user.auth_token.delete()
    except (AttributeError, ObjectDoesNotExist):
        pass

    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": "success"
        },
        status=HTTP_200_OK,
    )


# TODO: refactor
def extract_documents_from_queryset(documents_queryset):
    return list(
        map(
            lambda item: {
                "id": item.id,
                "title": item.title,
                "authors": list(
                    item.authors.values_list(
                        "name", flat=True
                    )
                ),
                "annotation": item.annotation,
                "keywords": list(item.keywords.names()),
                "publication_date": item.publication_date.isoformat(),
                "publishers": item.publishers.name,
            },
            list(documents_queryset),
        )
    )


# TODO: refactor
def extract_documents_by_year_from_queryset(documents_queryset):
    t_dict = {}
    total = 0
    data = {"items": []}

    for year in (
            documents_queryset
                    .annotate(year=ExtractYear("publication_date"))
                    .values_list("year", flat=True)
                    .distinct()
    ):
        t_dict[year] = extract_documents_from_queryset(
            documents_queryset.filter(publication_date__year=year)
        )

    for key, value in t_dict.items():
        data["items"].append(
            {
                "year": key,
                "items": value
            }
        )
        total += len(value)

    data["total"] = total

    return data


def get_documents_by_category(request, category):
    authors = request.query_params.get("authors")
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
    publishers = request.query_params.get("publish_places")
    text = request.query_params.get("text")

    db_request = Document.objects.filter(category=category)

    if authors is not None:
        db_request = db_request.filter(authors__name__in=authors.split(","))
    if start_date is not None:
        db_request = db_request.filter(publication_date__gte=start_date)
    if end_date is not None:
        db_request = db_request.filter(publication_date__lte=end_date)
    if publishers is not None:
        db_request = db_request.filter(publisher__name__in=publishers.split(","))
    if text is not None:
        db_request = db_request.filter(
            reduce(operator.and_, [Q(title__icontains=word) for word in text.split()])
            | reduce(operator.and_, [Q(annotation__icontains=word) for word in text.split()])
            | reduce(operator.and_, [Q(keywords__name__icontains=word) for word in text.split()])
        )

    db_request = db_request.order_by("-publication_date")

    data = extract_documents_by_year_from_queryset(db_request)

    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": data
        },
        status=HTTP_200_OK,
    )


# TODO: merge with `nir`
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def articles(request):
    return get_documents_by_category(
        request,
        Document.Category.ARTICLE,
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def nir(request):
    return get_documents_by_category(
        request,
        Document.Category.RESEARCH,
    )


# TODO: merge with `authors`
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def subjects(request):
    data = list(
        map(
            lambda x: {
                "id": x.id,
                "title": x.title
            },
            list(Subject.objects.all())
        )
    )
    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": data},
        status=HTTP_200_OK,
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def educational_materials(request):  # TODO: Добавить параметр айди предмета
    data = [
        {
            "id": 1,
            "title": "Матеша",
            "subject": {"id": 1, "title": "Subject"},
            "lectures": [
                {
                    "id": 1,
                    "title": "Справочник по матеше",
                    "url": "",
                    "edited": "2014-09-08T08:02:17-05:00",
                    "created": "2014-09-08T08:02:17-05:00",
                },
                {
                    "id": 2,
                    "title": "Справочник по матеше 2",
                    "url": "",
                    "edited": "2014-09-08T08:02:17-05:00",
                    "created": "2014-09-08T08:02:17-05:00",
                },
            ],
            "seminars": [
                {
                    "id": 1,
                    "title": "Семинар по матеше",
                    "url": "",
                    "edited": "2014-09-08T08:02:17-05:00",
                    "created": "2014-09-08T08:02:17-05:00",
                },
                {
                    "id": 2,
                    "title": "Семинар по матеше 2",
                    "url": "",
                    "edited": "2014-09-08T08:02:17-05:00",
                    "created": "2014-09-08T08:02:17-05:00",
                },
            ],
        }
    ]

    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": data
        },
        status=HTTP_200_OK,
    )


# TODO: merge with `published_places`
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def authors(request):
    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": list(
                map(
                    lambda x: {
                        "label": x,
                        "value": x
                    },
                    Profile.objects.all().values_list(
                        "name",
                        flat=True,
                    ),
                )
            ),
        },
        status=HTTP_200_OK,
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def published_places(request):
    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": list(
                map(
                    lambda x: {
                        "label": x,
                        "value": x
                    },
                    Publisher.objects.all().values_list(
                        "name",
                        flat=True,
                    ),
                )
            ),
        },
        status=HTTP_200_OK,
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def subject(request):
    return Response(
        {
            "code": HTTP_200_OK * 100,
            "data": {
                "parts": [
                    {
                        "title": "Титул",
                        "topics": [
                            {
                                "id": 1,
                                "title": "История развития",
                                "lectures": [{"name": "ЛР 2-1", "link": "https://google.com"}],
                                "seminars": [{"name": "СР 3-1", "link": "https://yandex.ru"}],
                                "group_classes": [
                                    {"name": "ГЗ 4-1", "link": "https://vk.com"},
                                    {"name": "ГЗ 4-2", "link": "https://yahoo.com"},
                                ],
                            }
                        ],
                    },
                    {
                        "title": "Имя",
                        "topics": [
                            {
                                "id": 1,
                                "title": "История развития",
                                "lectures": [
                                    {"name": "ЛР 2-1", "link": "https://google.com"},
                                    {"name": "ЛР 2-2", "link": "https://mail.com"},
                                    {"name": "ЛР 2-3", "link": "https://office.com"},
                                ],
                                "seminars": [{"name": "СР 3-1", "link": "https://yandex.ru"}],
                                "group_classes": [{"name": "ГЗ 4-1", "link": "https://vk.com"}],
                            }
                        ],
                    },
                    {
                        "title": "Титульник",
                        "topics": [
                            {
                                "id": 1,
                                "title": "История развития",
                                "lectures": [{"name": "ЛР 2-1", "link": "https://google.com"}],
                                "seminars": [
                                    {"name": "СР 3-1", "link": "https://yandex.ru"},
                                    {"name": "СР 3-2", "link": "https://yandex.ru"},
                                    {"name": "СР 3-3", "link": "https://yandex.ru"},
                                    {"name": "СР 3-4", "link": "https://yandex.ru"},
                                ],
                                "group_classes": [{"name": "ГЗ 4-1", "link": "https://vk.com"}],
                            }
                        ],
                    },
                    {
                        "title": "Название",
                        "topics": [
                            {
                                "id": 1,
                                "title": "История развития",
                                "lectures": [{"name": "ЛР 2-1", "link": "https://google.com"}],
                                "seminars": [{"name": "СР 3-1", "link": "https://yandex.ru"}],
                                "group_classes": [{"name": "ГЗ 4-1", "link": "https://vk.com"}],
                            }
                        ],
                    },
                    {
                        "title": "Введение",
                        "topics": [
                            {
                                "id": 1,
                                "title": "История развития",
                                "lectures": [{"name": "ЛР 2-1", "link": "https://google.com"}],
                                "seminars": [{"name": "СР 3-1", "link": "https://yandex.ru"}],
                                "group_classes": [{"name": "ГЗ 4-1", "link": "https://vk.com"}],
                            }
                        ],
                    },
                    {
                        "title": "Основная часть",
                        "topics": [
                            {
                                "id": 1,
                                "title": "Развитие истории",
                                "lectures": [{"name": "ЛР 2-1", "link": "https://google.com"}],
                                "seminars": [{"name": "СР 3-1", "link": "https://yandex.ru"}],
                                "group_classes": [{"name": "ГЗ 4-1", "link": "https://vk.com"}],
                            },
                            {
                                "id": 2,
                                "title": "История развития",
                                "lectures": [{"name": "ЛР 2-1", "link": "https://google.com"}],
                                "seminars": [{"name": "СР 3-1", "link": "https://yandex.ru"}],
                                "group_classes": [{"name": "ГЗ 4-1", "link": "https://vk.com"}],
                            },
                        ],
                    },
                ]
            },
        },
        status=HTTP_200_OK,
    )


# TODO: move to Document model
def delete_document(request):
    document_id = request.query_params.get("id")
    document = Document.objects.get(id=document_id)
    document.is_in_trash = True


# TODO: merge with `delete_nir`
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def delete_article(request):
    delete_document(request)
    return Response(
        {
            "code": HTTP_200_OK * 100
        },
        status=HTTP_200_OK,
    )


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def delete_nir(request):
    delete_document(request)
    return Response(
        {
            "code": HTTP_200_OK * 100
        },
        status=HTTP_200_OK,
    )