from rest_framework import serializers
from api.models import Admin, Disease, DiseaseExternalLink, Doctor, Medicine, Patient, DiseaseMedicine, PatientDiagnosis, PatientDiagnosisSymptom, Symptom


class AddDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        exclude = ['isApproved', 'approvingAdminId']


class DoctorDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        exclude = ['password']


class AddPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class PatientDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ['password']


class AdminDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        exclude = ['password']


class AddExternalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseExternalLink
        fields = '__all__'


class ExternalLinkDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseExternalLink
        fields = '__all__'


class AddMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'


class MedicineDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = '__all__'


class AddDiseaseMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseMedicine
        fields = '__all__'


# This one is used as a request body serializer for the disease prediction view
class SymptomIdsListSerializer(serializers.Serializer):
    symptomIds = serializers.ListField(child=serializers.IntegerField())


# This one is used as a request body serializer for add multiple medicines to a disease
class MedicineIdsListSerializer(serializers.Serializer):
    medicineIds = serializers.ListField(child=serializers.IntegerField())


# This one is used as a request body serializer for removing multiple medicines from a disease
class DiseaseMedicineIdsListSerializer(serializers.Serializer):
    diseaseMedicineIds = serializers.ListField(
        child=serializers.IntegerField())


class AddDiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDiagnosis
        exclude = ['diagnosisDateTime']


class AddPatientDiagnosisSymptomSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientDiagnosisSymptom
        fields = '__all__'


class SymptomDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        exclude = ['datasetName']


class DiseaseOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'


class DiseaseDetailsSerializer(serializers.ModelSerializer):
    externalLinks = serializers.SerializerMethodField(read_only=True)
    suggestedMedicines = serializers.SerializerMethodField(read_only=True)

    def get_externalLinks(self, disease):
        external_links = DiseaseExternalLink.objects.filter(
            diseaseId=disease.pk)
        return ExternalLinkDisplaySerializer(external_links, many=True).data

    def get_suggestedMedicines(self, disease):
        request = self.context.get('request')
        medicines = DiseaseMedicine.objects.filter(
            diseaseId=disease.pk)
        medicines = [medicine.medicineId for medicine in medicines]
        return MedicineDisplaySerializer(medicines, context={'request': request}, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'externalLinks': data.pop('externalLinks'),
            'suggestedMedicines': data.pop('suggestedMedicines'),
            'disease': data
        }

    class Meta:
        model = Disease
        fields = '__all__'


class DiagnosisDetailsSerializer(serializers.ModelSerializer):
    symptoms = serializers.SerializerMethodField(read_only=True)
    diseaseDetails = serializers.SerializerMethodField(read_only=True)

    def get_symptoms(self, patientDiagnosis):
        diagnosisSymptoms = PatientDiagnosisSymptom.objects.filter(
            patientDiagnosisId=patientDiagnosis.pk)
        diagnosisSymptoms = [
            diagnosisSymptom.symptomId for diagnosisSymptom in diagnosisSymptoms]
        return SymptomDisplaySerializer(diagnosisSymptoms, many=True).data

    def get_diseaseDetails(self, patientDiagnosis):
        request = self.context.get('request')
        return DiseaseDetailsSerializer(patientDiagnosis.diseaseId, context={'request': request}).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {
            'symptoms': data.pop('symptoms'),
            'diseaseDetails': data.pop('diseaseDetails'),
            'diagnosis': data
        }

    class Meta:
        model = PatientDiagnosis
        fields = '__all__'
