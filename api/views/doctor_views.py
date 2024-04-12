from api.models import Doctor, MedicalCase
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password


from api.serializers import AddDoctorSerializer, DoctorDisplaySerializer, MedicalCaseDetailsSerializer


@api_view(['POST'])
def registerNewDoctor(request):
    requestData = request.data
    if 'password' not in requestData.keys():
        return Response("Please provide a password", status=status.HTTP_400_BAD_REQUEST)

    plainPassword = requestData.get('password')
    hashedPassword = make_password(plainPassword)
    requestData._mutable = True
    requestData['password'] = hashedPassword

    addDoctorSerializer = AddDoctorSerializer(data=requestData)
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


@api_view(['GET'])
def getById(request, userId):
    user = Doctor.objects.filter(id=userId).first()
    if not user:
        return Response('Doctor not found', status=status.HTTP_404_NOT_FOUND)
    return Response(DoctorDisplaySerializer(user).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getMyMedicalCases(request, userId):
    newCases = MedicalCase.objects.filter(takenBy=userId).order_by('id')
    return Response(MedicalCaseDetailsSerializer(newCases, many=True).data)


@api_view(['GET'])
def getNewMedicalCases(request):
    newCases = MedicalCase.objects.filter(status='pending').order_by('id')
    return Response(MedicalCaseDetailsSerializer(newCases, many=True).data)


@api_view(['POST'])
def takeMedicalCase(request, caseId):
    doctorId = request.data.get('doctorId')

    if not doctorId:
        return Response('No doctor id was provided', status=status.HTTP_400_BAD_REQUEST)
    doctor = Doctor.objects.filter(id=doctorId).first()
    if not doctor:
        return Response('Doctor not found', status=status.HTTP_404_NOT_FOUND)
    medicalCase = MedicalCase.objects.filter(id=caseId).first()
    if not medicalCase:
        return Response('Medical Case not found, perhaps it was deleted', status=status.HTTP_404_NOT_FOUND)
    if medicalCase.status != 'pending':
        return Response('This case is already taken', status=status.HTTP_400_BAD_REQUEST)

    MedicalCase.objects.filter(id=caseId).update(
        status='taken', takenBy=doctorId)

    return Response(True)
