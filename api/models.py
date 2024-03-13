from django.db import models


class Admin(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Doctor(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=200)
    dateOfBirth = models.DateField()
    certificateUrl = models.ImageField(upload_to='doctor_certificates/')
    isApproved = models.BooleanField(default=False)
    approvingAdminId = models.ForeignKey(
        Admin, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.firstName + " " + self.lastName


class Patient(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=200)
    dateOfBirth = models.DateField()
    isMale = models.BooleanField()

    def __str__(self):
        return self.firstName + " " + self.lastName


class Disease(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class DiseaseExternalLink(models.Model):
    title = models.CharField(max_length=60)
    link = models.CharField(max_length=2000)
    diseaseId = models.ForeignKey(Disease, on_delete=models.CASCADE)

    def __str__(self):
        return self.diseaseId.name + " | " + self.title


class Medicine(models.Model):
    name = models.CharField(max_length=60)
    imageUrl = models.ImageField(upload_to='medicine_images/')

    def __str__(self):
        return self.name


class DiseaseMedicine(models.Model):
    diseaseId = models.ForeignKey(Disease, on_delete=models.CASCADE)
    medicineId = models.ForeignKey(Medicine, on_delete=models.CASCADE)

    def __str__(self):
        return self.diseaseId.name + " | " + self.medicineId.name
