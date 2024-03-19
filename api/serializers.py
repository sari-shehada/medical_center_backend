from rest_framework import serializers
from api.models import Admin, DiseaseExternalLink, Doctor, Medicine, Patient, DiseaseMedicine, PatientDiagnosis, PatientDiagnosisSymptom


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


class AddMedicineSerializer(serializers.ModelSerializer):
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
