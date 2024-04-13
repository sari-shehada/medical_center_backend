from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from api.models import MedicalCase, MedicalCaseMessage
from api.serializers import AddMedicalCaseMessageSerializer, MedicalCaseMessageDisplaySerializer


def fetchMedicalCaseMessages(caseId):
    messages = MedicalCaseMessage.objects.filter(caseId=caseId)
    return messages


@api_view(['GET'])
def getMedicalCaseMessages(request, caseId):
    messages = fetchMedicalCaseMessages(caseId=caseId)
    return Response(MedicalCaseMessageDisplaySerializer(messages, many=True).data)


@api_view(['POST'])
def sendMessageToMedicalCaseChat(request, caseId):
    requestData = request.data
    try:
        requestData._mutable = True
    except:
        print('not mutable')
    requestData['caseId'] = caseId
    addMessageSerializer = AddMedicalCaseMessageSerializer(data=requestData)
    medical_case = MedicalCase.objects.filter(id=caseId).first()
    if (not medical_case):
        return Response(status=status.HTTP_404_NOT_FOUND)
    if (medical_case.status == 'ended'):
        Response(
            MedicalCaseMessageDisplaySerializer(
                fetchMedicalCaseMessages(caseId=caseId),
                many=True
            ).data,
            status=status.HTTP_400_BAD_REQUEST
        )
    if addMessageSerializer.is_valid():
        addMessageSerializer.save()
        messages = fetchMedicalCaseMessages(caseId=caseId)
        return Response(MedicalCaseMessageDisplaySerializer(messages, many=True).data)
    return Response(addMessageSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
