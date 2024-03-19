from api.models import Admin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password

from api.serializers import AdminDisplaySerializer


@api_view(['POST'])
def loginAdmin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username == None:
        return Response("Please provide a username", status=status.HTTP_400_BAD_REQUEST)
    if password == None:
        return Response("Please provide a password", status=status.HTTP_400_BAD_REQUEST)

    try:
        admin = Admin.objects.get(username=username)
        if (check_password(password=password, encoded=admin.password)):
            return Response(AdminDisplaySerializer(admin).data)
        else:
            return Response(False)
    except Admin.DoesNotExist:
        return Response(False)
