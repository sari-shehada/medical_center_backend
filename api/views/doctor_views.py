from api.models import Doctor
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password


from api.serializers import AddDoctorSerializer, DoctorDisplaySerializer


@api_view(['POST'])
def registerNewDoctor(request):
    body = request.data
    if 'password' not in body.keys():
        return Response("Please provide a password", status=status.HTTP_400_BAD_REQUEST)

    plainPassword = body['password']
    body['password'] = make_password(plainPassword)
    addDoctorSerializer = AddDoctorSerializer(data=body)
    if addDoctorSerializer.is_valid():
        user = addDoctorSerializer.save()
        return Response(DoctorDisplaySerializer(user, context={'request': request}).data, status=status.HTTP_201_CREATED)
    return Response(addDoctorSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def loginDoctor(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username == None:
        return Response("Please provide a username", status=status.HTTP_400_BAD_REQUEST)
    if password == None:
        return Response("Please provide a password", status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Doctor.objects.get(username=username)
        if (check_password(password=password, encoded=user.password)):
            return Response(DoctorDisplaySerializer(user, context={'request': request}).data)
        else:
            return Response(False)
    except Doctor.DoesNotExist:
        return Response(False)
