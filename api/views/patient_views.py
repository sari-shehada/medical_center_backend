from api.models import MedicalCase, Patient, PatientDiagnosis
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password

from api.serializers import AddPatientSerializer, PatientDisplaySerializer, DiagnosisDetailsSerializer


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
        user = Patient.objects.get(username=username)
        if (check_password(password=password, encoded=user.password)):
            return Response(PatientDisplaySerializer(user, context={'request': request}).data)
        else:
            return Response(False)
    except Patient.DoesNotExist:
        return Response(False)


@api_view(['GET'])
def getById(request, userId):
    user = Patient.objects.filter(id=userId)
    if not user:
        return Response('User not found', status=status.HTTP_404_NOT_FOUND)
    return Response(PatientDisplaySerializer(user).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getDiagnosisHistory(request, userId):
    diagnostics = PatientDiagnosis.objects.filter(patientId=userId)
    return Response(DiagnosisDetailsSerializer(diagnostics, many=True).data, status=status.HTTP_200_OK)


@api_view(['POST'])
def submitNewMedicalCase(request, userId, diagnosisId):
    patientDiagnosis = PatientDiagnosis.objects.filter(id=diagnosisId).first()
    if not patientDiagnosis:
        return Response('This Diagnosis was not found, perhaps it was removed!', status=status.HTTP_404_NOT_FOUND)

    if patientDiagnosis.patientId.pk != userId:
        return Response('Invalid patient id provided', status=status.HTTP_400_BAD_REQUEST)

    if patientDiagnosis.isSubmittedForFurtherFollowup:
        return Response('Diagnosis already submitted for further follow-up', status=status.HTTP_400_BAD_REQUEST)

    MedicalCase.objects.create(diagnosisId=patientDiagnosis)
    PatientDiagnosis.objects.filter(id=diagnosisId).update(
        isSubmittedForFurtherFollowup=True)

    return Response('This diagnosis was submitted as a medical case', status=status.HTTP_200_OK)
