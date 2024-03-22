from api.models import Disease, DiseaseExternalLink, Symptom
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.serializers import AddExternalLinkSerializer, DiseaseDetailsSerializer, DiseaseOnlySerializer, SymptomDisplaySerializer


@api_view(['POST'])
def addExternalLinkToDisease(request):
    body = request.data
    addExternalLinkSerializer = AddExternalLinkSerializer(data=body)
    if addExternalLinkSerializer.is_valid():
        addExternalLinkSerializer.save()
        return Response(True, status=status.HTTP_201_CREATED)
    return Response(addExternalLinkSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def removeExternalLinkFromDisease(request, linkId):
    DiseaseExternalLink.objects.filter(id=linkId).delete()
    return Response(True, status=status.HTTP_200_OK)


@api_view(['GET'])
def getDiseasesList(request):
    includeDiseaseDetails = request.GET.get('includeDiseaseDetails')
    diseases = Disease.objects.all()
    if includeDiseaseDetails:
        return Response(DiseaseDetailsSerializer(diseases, many=True, context={
            'request': request
        }).data)
    return Response(DiseaseOnlySerializer(diseases, many=True).data)


@api_view(['GET'])
def getSymptomsList(request):
    symptoms = Symptom.objects.all()
    return Response(SymptomDisplaySerializer(symptoms, many=True).data, status=status.HTTP_200_OK)
