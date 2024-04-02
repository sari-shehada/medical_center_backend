from api.models import Admin, Disease, DiseaseMedicine, Medicine
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password

from api.serializers import AddMedicineSerializer, DiseaseMedicineIdsListSerializer, MedicineDisplaySerializer, MedicineIdsListSerializer


@api_view(['GET'])
def getAll(request):
    medicines = Medicine.objects.all()
    return Response(
        MedicineDisplaySerializer(medicines,
                                  many=True,
                                  context={'request': request}
                                  ).data
    )


@api_view(['POST'])
def addMedicine(request):
    body = request.data
    addMedicineSerializer = AddMedicineSerializer(data=body)
    if addMedicineSerializer.is_valid():
        addMedicineSerializer.save()
        return Response(True, status=status.HTTP_201_CREATED)
    return Response(addMedicineSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def addMedicinesToDisease(request, diseaseId):
    try:
        disease = Disease.objects.get(id=diseaseId)
    except Disease.DoesNotExist:
        return Response("Disease with this id was not found", status=status.HTTP_404_NOT_FOUND)
    body = request.data
    medicineIdsListSerializer = MedicineIdsListSerializer(data=body)
    if not medicineIdsListSerializer.is_valid():
        return Response(medicineIdsListSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    medicineIds = medicineIdsListSerializer.validated_data['medicineIds']
    medicines = Medicine.objects.filter(id__in=medicineIds)
    diseaseMedicines = DiseaseMedicine.objects.filter(diseaseId=diseaseId)
    alreadyAddedIds = [
        diseaseMedicine.medicineId.pk for diseaseMedicine in diseaseMedicines]

    for medicine in medicines:
        if not alreadyAddedIds.__contains__(medicine.pk):
            DiseaseMedicine(diseaseId=disease, medicineId=medicine).save()
    return Response(True, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def removeMedicinesFromDisease(request, diseaseId):
    body = request.data
    medicineIdsListSerializer = DiseaseMedicineIdsListSerializer(data=body)
    if not medicineIdsListSerializer.is_valid():
        return Response(medicineIdsListSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    diseaseMedicineIds = medicineIdsListSerializer.validated_data['diseaseMedicineIds']
    DiseaseMedicine.objects.filter(
        id__in=diseaseMedicineIds, diseaseId=diseaseId).delete()
    return Response(True, status=status.HTTP_200_OK)
