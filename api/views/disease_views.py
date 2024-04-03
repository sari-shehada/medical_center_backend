import random
from api.models import Disease, DiseaseExternalLink, Symptom
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.serializers import AddExternalLinkSerializer, DiseaseDetailsSerializer, DiseaseOnlySerializer, ExternalLinkDetailsSerializer, ExternalLinkDisplaySerializer, SymptomDisplaySerializer


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


@api_view(['GET'])
def getReadingList(request):
    ids = DiseaseExternalLink.objects.values_list('pk', flat=True)
    ids = sorted(ids)
    sampleSize = 25
    selectedIds = random.sample(
        ids, k=sampleSize if len(ids) > sampleSize else len(ids))
    external_links = DiseaseExternalLink.objects.filter(id__in=selectedIds)
    external_links = list(external_links)
    random.shuffle(external_links)
    return Response(ExternalLinkDetailsSerializer(external_links, many=True, context={
        'request': request
    }).data)


@api_view(['POST'])
def getExternalLinksForDisease(request, diseaseId):
    links = DiseaseExternalLink.objects.filter(diseaseId=diseaseId)
    return Response(ExternalLinkDisplaySerializer(links, many=True, context={
        'request': request
    }).data, status=status.HTTP_200_OK)
