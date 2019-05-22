from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT
)


def response_200(data):
    return Response(data, status=HTTP_200_OK)


def response_201(data):
    return Response(data, status=HTTP_201_CREATED)


def response_204(data):
    return Response(data, status=HTTP_204_NO_CONTENT)


def response_400(data, msg='Invalid Params'):
    if isinstance(data, dict):
        _data = {k: str(v[0]) if isinstance(v, list) else v for k, v in data.items()}
    else:
        _data = data
    return Response({"msg": msg, "detailInfo": _data}, status=HTTP_400_BAD_REQUEST)


def response_404(msg='Not Found'):
    return Response({"msg": msg}, status=HTTP_404_NOT_FOUND)
