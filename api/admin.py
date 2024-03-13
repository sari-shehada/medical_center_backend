from django.contrib import admin

from api.models import Admin, Disease, DiseaseExternalLink, DiseaseMedicine, Doctor, Medicine, Patient

admin.site.register(Doctor)
admin.site.register(Admin)
admin.site.register(Patient)
admin.site.register(Medicine)
admin.site.register(Disease)
admin.site.register(DiseaseMedicine)
admin.site.register(DiseaseExternalLink)
