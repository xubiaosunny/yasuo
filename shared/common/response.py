from rest_framework.response import Response


def _response_20x(data=None, status=200):
    return Response(data, status=status)


def response_200(data):
    return _response_20x(data, status=200)


def response_201(data):
    return _response_20x(data, status=201)


def response_204(data):
    return _response_20x(data, status=204)


def response_400(data, msg='Invalid Params'):
    return Response({"msg": msg, "detail": data}, status=400)
