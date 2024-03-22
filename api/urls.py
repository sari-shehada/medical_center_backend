from django.urls import include, path

from api.views import doctor_views, patient_views, admin_views, disease_views, medicine_views, disease_prediction_views

api_urls = [
    # Admin end-points
    path('admins/login/', admin_views.loginAdmin),
    path('doctors/pending/', admin_views.getPendingDoctors),
    path('doctors/<int:doctorId>/approveApplication/',
         admin_views.approveDoctorApplication),
    path('doctors/<int:doctorId>/rejectApplication/',
         admin_views.rejectDoctorApplication),



    path('symptoms/', disease_views.getSymptomsList),
    path('diseases/', disease_views.getDiseasesList),

    # Adding and removing external links to diseases
    path('externalLinks/new/', disease_views.addExternalLinkToDisease),
    path('externalLinks/<int:linkId>/delete/',
         disease_views.removeExternalLinkFromDisease),


    # Adding and removing medicines to diseases
    path('medicines/new/', medicine_views.addMedicine),
    path('disease/<int:diseaseId>/addMedicines/',
         medicine_views.addMedicinesToDisease),
    path('disease/<int:diseaseId>/removeMedicines/',
         medicine_views.removeMedicinesFromDisease),

    # Doctor end-points
    path('doctors/new/', doctor_views.registerNewDoctor),
    path('doctors/login/', doctor_views.loginDoctor),
    path('medicalCases/', doctor_views.getNewMedicalCases),
    path('medicalCases/<int:caseId>/takeCase/', doctor_views.takeMedicalCase),

    # Patient end-points
    path('patients/new/', patient_views.registerNewPatient),
    path('patients/login/', patient_views.loginPatient),
    path('patients/<int:userId>/diagnosisHistory/',
         patient_views.getDiagnosisHistory),
    path('patients/<int:userId>/diagnoseDisease/',
         disease_prediction_views.diagnoseDisease),
    path('patients/<int:userId>/diagnostics/<int:diagnosisId>/submitMedicalCase/',
         patient_views.submitNewMedicalCase),
]
