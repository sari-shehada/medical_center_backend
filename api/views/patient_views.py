from api.models import Patient
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password

from api.serializers import AddPatientSerializer, PatientDisplaySerializer


@api_view(['POST'])
def registerNewPatient(request):
    body = request.data.dict()
    if 'password' not in body.keys():
        return Response("Please provide a password", status=status.HTTP_400_BAD_REQUEST)

    plainPassword = body['password']
    body['password'] = make_password(plainPassword)
    addPatientSerializer = AddPatientSerializer(data=body)
    if addPatientSerializer.is_valid():
        user = addPatientSerializer.save()
        return Response(PatientDisplaySerializer(user, context={'request': request}).data, status=status.HTTP_201_CREATED)
    return Response(addPatientSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def loginPatient(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username == None:
        return Response("Please provide a username", status=status.HTTP_400_BAD_REQUEST)
    if password == None:
        return Response("Please provide a password", status=status.HTTP_400_BAD_REQUEST)

    try:
        user = doctor = Patient.objects.get(username=username)
        if (check_password(password=password, encoded=user.password)):
            return Response(PatientDisplaySerializer(user, context={'request': request}).data)
        else:
            return Response(False)
    except Patient.DoesNotExist:
        return Response(False)
