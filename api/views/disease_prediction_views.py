import json
import os
import joblib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models import Disease, Patient, Symptom
from api.serializers import AddDiagnosisSerializer, AddPatientDiagnosisSymptomSerializer, DiagnosisDetailsSerializer, SymptomIdsListSerializer
import pandas as pd
import pickle

from api.definitions import API_APP_DIR


model_path = os.path.join(API_APP_DIR, 'ai_model/classification_model.pkl')
ordered_symptoms_path = os.path.join(
    API_APP_DIR, 'ai_model/columns_order.json')

classification_model = joblib.load(model_path)


@api_view(['POST'])
def diagnoseDisease(request, userId):
    serializer = SymptomIdsListSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    try:
        Patient.objects.get(id=userId)
    except Patient.DoesNotExist:
        return Response('Patient not found', status=status.HTTP_404_NOT_FOUND)

    symptom_ids = serializer.validated_data['symptomIds']
    symptoms = Symptom.objects.filter(id__in=symptom_ids)
    symptomDatasetNames = [
        symptomName.datasetName for symptomName in symptoms]
    diagnosis, confidence = predictDisease(symptoms=symptomDatasetNames)
    patientDiagnosis = logUserDiagnosis(
        userId=userId, diagnosis=diagnosis, symptoms=symptoms)
    return Response(
        DiagnosisDetailsSerializer(patientDiagnosis, context={'request': request}).data)


def makePredictionDataFrame(symptomDatasetNames):
    with open(ordered_symptoms_path, 'r') as file:
        symptoms = json.load(file)
    inputData = {key: 0 for key in symptoms}
    for symptom in symptomDatasetNames:
        inputData[symptom] = 1

    dataFrame = pd.DataFrame(inputData, index=[0])
    dataFrame = dataFrame.reindex(columns=symptoms)
    return dataFrame


def predictDisease(symptoms):
    model_input = makePredictionDataFrame(symptomDatasetNames=symptoms)
    prediction = classification_model.predict(model_input)
    probability = classification_model.predict_proba(
        model_input).max()
    return prediction[0], probability


def logUserDiagnosis(userId, diagnosis, symptoms):
    disease = Disease.objects.filter(datasetName=diagnosis).first()
    if not disease:
        return
    addDiagnosisSerializer = AddDiagnosisSerializer(data={
        'patientId': userId,
        'diseaseId': disease.pk
    })
    if (addDiagnosisSerializer.is_valid()):
        patientDiagnosis = addDiagnosisSerializer.save()
    else:
        return
    for symptom in symptoms:
        addDiagnosisSymptomSerializer = AddPatientDiagnosisSymptomSerializer(data={
            "patientDiagnosisId": patientDiagnosis.pk,
            "symptomId": symptom.pk
        })
        if (addDiagnosisSymptomSerializer.is_valid()):
            addDiagnosisSymptomSerializer.save()
    return patientDiagnosis
