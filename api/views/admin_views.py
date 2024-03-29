from api.models import Admin, Doctor
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password, make_password

from api.serializers import AdminDisplaySerializer, DoctorDisplaySerializer


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


@api_view(['POST'])
def getById(request, adminId):
    user = Admin.objects.filter(id=adminId)
    if not user:
        return Response('Admin not found', status=status.HTTP_404_NOT_FOUND)
    return Response(AdminDisplaySerializer(user).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getPendingDoctors(request):
    pending_doctors = Doctor.objects.filter(isApproved=False)
    return Response(DoctorDisplaySerializer(pending_doctors, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


@api_view(['POST'])
def approveDoctorApplication(request, doctorId):
    adminId = request.data.get('adminId')
    if adminId is None:
        return Response("No Admin Id was provided", status=status.HTTP_400_BAD_REQUEST)

    doctor = Doctor.objects.filter(id=doctorId).first()
    if doctor is None:
        return Response("Doctor not found", status=status.HTTP_404_NOT_FOUND)
    if doctor.isApproved == True:
        return Response("This Doctor is already approved", status=status.HTTP_400_BAD_REQUEST)
    Doctor.objects.filter(id=doctorId).update(
        isApproved=True, approvingAdminId=adminId)
    return Response(True, status=status.HTTP_200_OK)


@api_view(['POST'])
def rejectDoctorApplication(request, doctorId):
    doctor = Doctor.objects.filter(id=doctorId).first()
    if doctor is None:
        return Response("Doctor not found", status=status.HTTP_404_NOT_FOUND)
    if doctor.isApproved == True:
        return Response("This doctor is already approved, cannot reject", status=status.HTTP_400_BAD_REQUEST)
    Doctor.objects.filter(id=doctorId).delete()
    return Response(True, status=status.HTTP_200_OK)
