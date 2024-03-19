from api.models import Admin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password

from api.serializers import AddExternalLinkSerializer


@api_view(['POST'])
def addExternalLinkToDisease(request):
    body = request.data
    addExternalLinkSerializer = AddExternalLinkSerializer(data=body)
    if addExternalLinkSerializer.is_valid():
        addExternalLinkSerializer.save()
        return Response(True, status=status.HTTP_201_CREATED)
    return Response(addExternalLinkSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
