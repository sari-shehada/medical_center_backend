from django.urls import include, path

from api.views import doctor_views, patient_views

api_urls = [
    # Doctor end-points
    path('doctors/new/', doctor_views.registerNewDoctor),
    path('doctors/login/', doctor_views.loginDoctor),


    # Patient end-points
    path('patients/new/', patient_views.registerNewPatient),
    path('patients/login/', patient_views.loginPatient),
]
