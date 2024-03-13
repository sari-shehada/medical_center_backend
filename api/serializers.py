from rest_framework import serializers
from api.models import Doctor, Patient


class AddDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        exclude = ('isApproved', 'approvingAdminId')


class DoctorDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        exclude = ('isApproved', 'password')


class AddPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class PatientDisplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        exclude = ('password')
