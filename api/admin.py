from django.contrib import admin

from api.models import Admin, Disease, MedicalCaseMessage, DiseaseExternalLink, MedicalCase, DiseaseMedicine, Doctor, Medicine, Patient, Symptom, PatientDiagnosis, PatientDiagnosisSymptom

admin.site.register(Doctor)
admin.site.register(Admin)
admin.site.register(Patient)
admin.site.register(Medicine)
admin.site.register(Disease)
admin.site.register(DiseaseMedicine)
admin.site.register(DiseaseExternalLink)
admin.site.register(Symptom)
admin.site.register(PatientDiagnosis)
admin.site.register(PatientDiagnosisSymptom)
admin.site.register(MedicalCase)
admin.site.register(MedicalCaseMessage)
