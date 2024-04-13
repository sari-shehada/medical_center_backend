from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from api.models import MedicalCase, MedicalCaseMessage
from api.serializers import AddMedicalCaseMessageSerializer, MedicalCaseMessagesSerializer


@api_view(['GET'])
def getMedicalCaseMessages(request, caseId):
    medical_case = MedicalCase.objects.filter(id=caseId).first()
    if (not medical_case):
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(MedicalCaseMessagesSerializer(medical_case).data)


@api_view(['POST'])
def sendMessageToMedicalCaseChat(request, caseId):
    requestData = request.data
    try:
        requestData._mutable = True
    finally:
        requestData['caseId'] = caseId
    medical_case = MedicalCase.objects.filter(id=caseId).first()
    if (not medical_case):
        return Response(status=status.HTTP_404_NOT_FOUND)
    if (medical_case.status == 'ended'):
        return Response(MedicalCaseMessagesSerializer(medical_case).data, status=status.HTTP_400_BAD_REQUEST)
    addMessageSerializer = AddMedicalCaseMessageSerializer(data=requestData)
    if addMessageSerializer.is_valid():
        addMessageSerializer.save()
        Response(MedicalCaseMessagesSerializer(medical_case).data)
    return Response(addMessageSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
